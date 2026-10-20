from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import pandas as pd
import numpy as np
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64

from core.models import init_db, Project, SessionLocal
from core.engine import SMARTEngine, SMARTInput

# Identitas pembuat (tampil di footer). Silakan sesuaikan.
NAMA_MAHASISWA = "Solehudin Thaib"
NIM_MAHASISWA = "231011450099"
KELAS_MAHASISWA = "06TPLE003"

app = Flask(__name__)
app.secret_key = "smart_unpam_secret"
init_db()
engine = SMARTEngine()

@app.context_processor
def inject_identity():
    return {"nama_mahasiswa": NAMA_MAHASISWA, "nim_mahasiswa": NIM_MAHASISWA,
            "kelas_mahasiswa": KELAS_MAHASISWA}

def build_input(p_data):
    return SMARTInput(
        alternatives=p_data['alternatives'], criteria=p_data['criteria'],
        performance=np.array(p_data['performance']), weights_raw=np.array(p_data['weights']),
        types=p_data['types'], weight_method=p_data.get('weight_method', 'direct'),
        utility_mode=p_data.get('utility_mode', 'data'),
        scale_min=p_data.get('scale_min', 0.0), scale_max=p_data.get('scale_max', 100.0)
    )

def group_winners(p_data, scores):
    """Alternatif dengan skor tertinggi di tiap kelompok (mis. per kelas)."""
    groups = p_data.get('groups') or []
    if not any(groups):
        return []
    best = {}
    for i, g in enumerate(groups):
        if g and (g not in best or scores[i] > scores[best[g]]):
            best[g] = i
    return [(g, i) for g, i in best.items()]

@app.route('/')
def index():
    with SessionLocal() as db:
        projects = db.query(Project).all()
    return render_template('index.html', projects=projects)

@app.route('/materi')
def view_materi():
    return render_template('materi.html')

@app.route('/project/create', methods=['POST'])
def create_project():
    name = request.form.get('name')
    desc = request.form.get('description')
    default_data = {
        "criteria": ["Biaya", "Kualitas", "Fleksibilitas"],
        "types": ["cost", "benefit", "benefit"],
        "weights": [40.0, 40.0, 20.0],
        "weight_method": "direct",
        "utility_mode": "data",
        "alternatives": ["Vendor A", "Vendor B"],
        "groups": ["", ""],
        "performance": [[150, 80, 70], [120, 75, 85]]
    }
    with SessionLocal() as db:
        if db.query(Project).filter(Project.name == name).first():
            flash("Nama proyek sudah digunakan!", "danger")
        else:
            new_p = Project(name=name, description=desc, data_json=default_data)
            db.add(new_p)
            db.commit()
    return redirect(url_for('index'))

@app.route('/project/<int:id>')
def view_project(id):
    with SessionLocal() as db:
        project = db.get(Project, id)
    if not project: return "Proyek tidak ditemukan", 404
    return render_template('project.html', project=project, data=project.data_json)

@app.route('/project/<int:id>/update', methods=['POST'])
def update_data(id):
    criteria = request.form.getlist('criteria[]')
    types = request.form.getlist('types[]')
    weights = [float(w) for w in request.form.getlist('weights[]')]
    alternatives = request.form.getlist('alternatives[]')
    groups = [g.strip() for g in request.form.getlist('groups[]')]
    weight_method = request.form.get('weight_method', 'direct')
    utility_mode = request.form.get('utility_mode', 'data')
    scale_min = float(request.form.get('scale_min') or 0)
    scale_max = float(request.form.get('scale_max') or 100)

    if utility_mode == 'scale' and scale_max <= scale_min:
        flash("Nilai maksimum skala harus lebih besar dari nilai minimum.", "danger")
        return redirect(url_for('view_project', id=id))

    perf_flat = [float(p) for p in request.form.getlist('perf[]')]
    performance = np.array(perf_flat).reshape(len(alternatives), len(criteria)).tolist()

    updated_json = {
        "criteria": criteria, "types": types, "weights": weights,
        "weight_method": weight_method,
        "utility_mode": utility_mode, "scale_min": scale_min, "scale_max": scale_max,
        "alternatives": alternatives, "groups": groups, "performance": performance
    }

    with SessionLocal() as db:
        proj = db.get(Project, id)
        proj.data_json = updated_json
        db.commit()

    flash("Data Proyek Berhasil Diperbarui!", "success")
    return redirect(url_for('view_project', id=id))

@app.route('/project/<int:id>/upload', methods=['POST'])
def upload_file(id):
    file = request.files.get('file')
    if not file:
        flash("File tidak ditemukan", "danger")
        return redirect(url_for('view_project', id=id))

    df = pd.read_csv(file) if file.filename.endswith('.csv') else pd.read_excel(file)
    alts = df.iloc[:, 0].astype(str).tolist()
    criteria = df.columns[1:].tolist()
    performance = df.iloc[:, 1:].values.astype(float).tolist()

    with SessionLocal() as db:
        proj = db.get(Project, id)
        current_data = dict(proj.data_json)
        current_data["criteria"] = criteria
        current_data["types"] = ["benefit"] * len(criteria)
        current_data["weights"] = [100.0 / len(criteria)] * len(criteria)
        current_data["weight_method"] = "direct"
        current_data["alternatives"] = alts
        current_data["groups"] = [""] * len(alts)
        current_data["performance"] = performance
        proj.data_json = current_data
        db.commit()

    flash("Data Berhasil Diunggah!", "success")
    return redirect(url_for('view_project', id=id))

@app.route('/project/<int:id>/calculate')
def calculate_project(id):
    with SessionLocal() as db:
        proj = db.get(Project, id)
    if not proj: return "Proyek tidak ditemukan", 404
    p_data = proj.data_json

    inp = build_input(p_data)
    results = engine.calculate(inp)

    target_idx = request.args.get('target', 0, type=int)
    if not 0 <= target_idx < len(p_data['criteria']):
        target_idx = 0
    w_vals, scores_history = engine.run_oat_sensitivity(inp, target_idx)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors = plt.cm.tab20(np.linspace(0, 1, max(len(p_data['alternatives']), 2)))
    best_idx = results['ranking_indices'][0]
    for i, name in enumerate(p_data['alternatives']):
        alt_scores = [step[i] for step in scores_history]
        lw = 2.6 if i == best_idx else 1.3
        ax.plot(w_vals, alt_scores, linestyle='-', linewidth=lw, color=colors[i], label=name)
    base_w = results['normalized_weights'][target_idx]
    ax.axvline(base_w, color='#0f766e', linestyle='--', linewidth=1.2)
    ax.set_xlabel(f"Bobot kriteria {p_data['criteria'][target_idx]} (garis putus = bobot awal {base_w:.2f})", fontsize=9)
    ax.set_ylabel("Skor SMART V(a_i)", fontsize=9)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    ax.grid(True, axis='y', alpha=0.25)
    ax.legend(fontsize=7, loc='center left', bbox_to_anchor=(1.0, 0.5), frameon=False)

    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', bbox_inches='tight')
    img_buf.seek(0)
    plt.close()

    chart_base64 = base64.b64encode(img_buf.getvalue()).decode('utf-8')
    winners = group_winners(p_data, results['final_scores'])
    return render_template('results.html', project=proj, data=p_data, res=results, chart=chart_base64,
                           target_idx=target_idx, winners=winners)

@app.route('/project/<int:id>/export')
def export_excel(id):
    with SessionLocal() as db:
        proj = db.get(Project, id)
    p_data = proj.data_json
    df = pd.DataFrame(p_data['performance'], columns=p_data['criteria'], index=p_data['alternatives'])
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Matriks')
    output.seek(0)
    return send_file(output, as_attachment=True, download_name=f"Data_SMART_{proj.name}.xlsx")

@app.route('/project/<int:id>/delete')
def delete_project(id):
    with SessionLocal() as db:
        proj = db.get(Project, id)
        if proj:
            db.delete(proj)
            db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
