from abc import abstractproperty
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
from .models import Note, WallDesign
from . import db
import json
from .calculations import retaining_wall_calculations

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("notes.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted!', category='error')
    return jsonify({}) #return an empty respond

@views.route('/wall-designs', methods=['GET', 'POST'])
@login_required
def wall_designs():
    if request.method == 'POST':
        design = request.form.get('design-name')
        if len(design) < 1:
            flash('Design name is too short!', category='error')
            # verify the data quality
        else:
            new_design = WallDesign(design_name=design, user_id=current_user.id)
            db.session.add(new_design)
            db.session.commit()
            flash('Design added!', category='success')
    return render_template("wall_designs.html", user=current_user)

@views.route('/delete-design', methods=['POST'])
def delete_design():
    design = json.loads(request.data)
    designId = design['designId']
    design = WallDesign.query.get(designId)
    if design:
        if design.user_id == current_user.id:
            db.session.delete(design)
            db.session.commit()
            flash('Design deleted!', category='error')
    return jsonify({}) #return an empty respond

@views.route('/wall-designs/<variable>', methods=['GET', 'POST'])
@login_required
def retaining_wall(variable):
    design = WallDesign.query.filter_by(id=variable).first()
    if not design:
        abort(404)
    if current_user.id != design.user_id:
        abort(404)
    if request.method == 'GET':
        if design.gs and design.gb and design.phi and design.bc and design.bb and design.bh \
            and design.p and design.H and design.B:
            problem = {'gs':design.gs, 'gb':design.gb, 'phi':design.phi, 'bc':design.bc, 'bb':design.bb,
                'bh':design.bh, 'p':design.p, 'H':design.H, 'B':design.B}
            results = retaining_wall_calculations.dry_horizontal_back_retaining_wall_calculate(problem)
            return render_template("retaining_wall.html", user=current_user, design=design, results=results)
        else:
            return render_template("retaining_wall.html", user=current_user, design=design)
    if request.method == 'POST':
        gs = float(request.form.get('gs'))
        gb = float(request.form.get('gb'))
        phi = float(request.form.get('phi'))
        bc = float(request.form.get('bc'))
        bb = float(request.form.get('bb'))
        bh = float(request.form.get('bh'))
        p = float(request.form.get('p'))
        H = float(request.form.get('H'))
        B = float(request.form.get('B'))
        if gs<1.0 or gb<1.0 or phi<0.01 or bc==0.0 or bb==0.0 or bh==0.0 or p==0.0 or H==0.0 or B==0.0:
            flash('Not valid values!', category='error')
        else:
            design.gs = gs
            design.gb = gb
            design.phi = phi
            design.bc = bc
            design.bb = bb
            design.bh = bh
            design.p = p
            design.H = H
            design.B = B
            db.session.commit()
            flash('Design values were saved and model was analyzed!', category='success')
        
        # Defining the problem
        problem = {'gs':gs, 'gb':gb, 'phi':phi, 'bc':bc, 'bb':bb,
        'bh':bh, 'p':p, 'H':H, 'B':B}
        results = retaining_wall_calculations.dry_horizontal_back_retaining_wall_calculate(problem)
        return render_template("retaining_wall.html", user=current_user, 
        design=design, results=results)
