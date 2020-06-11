import flywheel
import glob
import os
import zipfile
import shutil

# 0. handling user input
context = flywheel.GearContext()  # Get the gear context
config = context.config           # from the gear context, get the config settings

target_project = config['target_project']
subject_label = config['subject_label']
session_label = config['session_label']
acquisition_label = config['acquisition_label']
user_id = 'stanfordlabs.flywheel.io:' + config['user_id']

# 1. Login Flywheel by user_id
fw = flywheel.Client(user_id)
self = fw.get_current_user()

# 2.create a temporary directory to place the files in the zipfile.
message_file = context.get_input_path('files')
print(message_file, type(message_file))

# 3. (original version) UPLOAD all INPUT files that are .dat or .txt
# However, this method will only deal with the files in the fist layer.
# upload_files = list(glob.glob(os.path.join("temp/", '*.dat')))
# upload_files.extend(glob.glob(os.path.join("temp/", '*.txt')))

# 3. Using the function below, we can get a list of all files in the zip file.
# This function is used to list all files recursively. it'll return a list that contains all files under a specific directory
def listall(root, path):
    #print(os.path.join(path,root))
    if not os.path.isdir(os.path.join(path,root)):
        return [os.path.join(path,root)]
    items = os.listdir(os.path.join(path,root))
    all = []
    for item in items:
        all.extend(listall(item, os.path.join(path,root)))
    return all

# 4. check the accuracy of the input(the existence of subject, session and acquisition)
try:
    project = fw.lookup(target_project)
except flywheel.ApiException as e:
    print('No project exist. You may just try again')
    raise

subjects = project.subjects()
subject = None
for i in subjects:
    if i.label == subject_label:
        print('Subject exist.')
        subject = i
assert subject is not None, 'No subject exist'

sessions = subject.sessions()
session = None
for i in sessions:
    if i.label == session_label:
        print('Session exist.')
        session = i
assert session is not None, 'No session exist'

acquisitions = session.acquisitions()
target_acqusition = None
for i in acquisitions:
    if i.label == acquisition_label:
        print('Acquisition exist')
        target_acqusition = i
assert target_acqusition != None, "No acquisition exist."




# 5. Upload files. After uploading is done, remove the temporary directory.
print('Uploading files...')
print('\t%s...' % (message_file))
target_acqusition.upload_file(message_file)
print('Done!')
