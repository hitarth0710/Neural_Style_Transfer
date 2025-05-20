from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_file
from flask_login import login_required, current_user
from app import db
from app.style_transfer.forms import StyleTransferForm, StyleTransferIndexForm
from app.style_transfer.utils import save_uploaded_file, perform_style_transfer
from app.style_transfer.models import StyleImage
import os
import uuid
from datetime import datetime, timedelta

style_transfer = Blueprint('style_transfer', __name__)

@style_transfer.route('/')
def index():
    # Remove the form reference that's causing the error
    # form = StyleTransferIndexForm()  
    # Instead, just render the template without a form
    form = StyleTransferIndexForm()
    return render_template('style_transfer/index.html', title='Home', form=form)

@style_transfer.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    form = StyleTransferForm()
    if form.validate_on_submit():
        try:
            # Save the uploaded files
            content_filename = save_uploaded_file(form.content_image.data)
            style_filename = save_uploaded_file(form.style_image.data)
            
            # Generate a unique filename for the result
            result_filename = f"uploads/{uuid.uuid4()}.png"
            
            # Generate absolute paths
            content_path = os.path.join(current_app.root_path, 'static', content_filename)
            style_path = os.path.join(current_app.root_path, 'static', style_filename)
            result_path = os.path.join(current_app.root_path, 'static', result_filename)

            style_strength = form.style_strength.data if form.style_strength.data else 0.75
            style_prompt = form.style_prompt.data if form.style_prompt.data else None
            
            # Perform style transfer
            perform_style_transfer(
                content_path,
                style_path,
                result_path,
                style_strength=style_strength,
                style_prompt=style_prompt
            )
            
            # Save to database
            style_image = StyleImage(
                content_image=content_filename,
                style_image=style_filename,
                result_image=result_filename,
                style_prompt=style_prompt,
                style_strength=style_strength,
                user_id=current_user.id
            )
            db.session.add(style_image)
            db.session.commit()
            
            flash('Style transfer completed successfully!', 'success')
            return redirect(url_for('style_transfer.results', image_id=style_image.id))
        
        except Exception as e:
            flash(f'Error during style transfer: {str(e)}', 'danger')
            return redirect(url_for('style_transfer.transfer'))
    
    return render_template('style_transfer/transfer.html', title='Transfer Style', form=form)

@style_transfer.route('/results/<int:image_id>')
@login_required
def results(image_id):
    style_image = StyleImage.query.get_or_404(image_id)
    
    # Ensure user can only view their own results
    if style_image.user_id != current_user.id:
        flash('You do not have permission to view this result.', 'danger')
        return redirect(url_for('style_transfer.index'))
    
    return render_template('style_transfer/results.html', title='Results', style_image=style_image)

@style_transfer.route('/gallery')
@login_required
def gallery():
    page = request.args.get('page', 1, type=int)
    images = StyleImage.query.filter_by(user_id=current_user.id).order_by(StyleImage.created_at.desc()).paginate(
        page=page, per_page=9)
    return render_template('style_transfer/gallery.html', title='Your Gallery', images=images)

@style_transfer.route('/download/<int:image_id>')
@login_required
def download_result(image_id):
    style_image = StyleImage.query.get_or_404(image_id)
    
    # Ensure the user can only download their own images
    if style_image.user_id != current_user.id:
        flash('You do not have permission to download this image.', 'danger')
        return redirect(url_for('style_transfer.index'))
    
    # Get the full path of the image
    image_path = os.path.join(current_app.root_path, style_image.result_image)
    
    # Return the file as an attachment (forces download)
    return send_file(image_path, as_attachment=True, download_name=f"style_transfer_{style_image.id}.png")


