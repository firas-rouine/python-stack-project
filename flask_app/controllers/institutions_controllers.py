from flask_app import app,IMAGES_PATH
from flask import  render_template,request, redirect, session,flash
from flask_app.models.institution_model import Institution
from flask_app.models.address_model import Address
from flask_app.models.user import User
from flask_app.models.institution_model import Institution
from flask_app.models.images_model import Image
import os,re
import urllib.request
from werkzeug.utils import secure_filename
UPLOAD_FOLDER='flask_app/static/uploads/'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS




# ? ========== Add Institution PAGE ==========

@app.route("/add_institution")
def show_form():
    user=User.get_by_id({'id':session['user_id']})
    image=IMAGES_PATH+user.image
    # print('😍😍😍',user.image,'😍😍❤')
    instituion=Institution.get_by_id_creator({'id':session['user_id']})

    return render_template('institution.html',user=user,institution=instituion,image=image)

# * ========== create institution --- ACTION

@app.route("/creators/institution", methods=["POST","GET"])
def create():
    if not Institution.validate(request.form):
        if not Address.validate(request.form):
            return redirect("/add_institution")
        return redirect("/add_institution")
    
    
    data = {
        **request.form,
        "creator_id" : session['user_id']
    }

    # Save the institution in DB
    institution_id = Institution.create(data)
    data["institution_id"] = institution_id
    Address.create(data)
    print("dataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",data)
    # ! *************add images**************
    if request.method=='POST':
        files = request.files.getlist('files[]')
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                data['name_image']=filename
                session['image']=IMAGES_PATH+filename
                print('session imageeeeeeeeeeeeeeeeeeeeeeeeeee',session['image'])
                img=Image.create(data)
                
        flash('files succesfully uploaded')
        return redirect('/add_institution')
    # ! *************************************
    return redirect('/add_institution')
    


