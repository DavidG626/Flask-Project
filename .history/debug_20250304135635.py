@progress_note_bp.route('/debug/<int:note_id>')
@login_required
def debug_note(note_id):
    note = ProgressNote.query.get(note_id)
    cpt_relations = ProgressNoteCPT.query.filter_by(progress_note_id=note_id).all()
    result = []
    for rel in cpt_relations:
        cpt = CPTCode.query.get(rel.cpt_id)
        if cpt:
            result.append(f"CPT {cpt.code}: {cpt.description}")
    return str(result)