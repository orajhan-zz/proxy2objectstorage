from flask import *
from flask_cors import CORS
import oci

app = Flask(__name__)
CORS(app)

@app.route('/image', methods=['GET'])
def index():
    # get objec and bucket name from url
    object = request.args.get('object')
    bucket = request.args.get('bucket')

    # Option 1. config file  ( I am locally testing this out)
    configfile = "your_path/config"
    config = oci.config.from_file(configfile)
    object_storage = oci.object_storage.ObjectStorageClient(config)
    namespace = object_storage.get_namespace().data

    # Option 2. get signer from instance principals in VM in OCI
    #signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
    # initialize the ObjectStorageClient with an empty config and only a signer
    #object_storage = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    #namespace = object_storage.get_namespace().data

    # Review parameters to access object storage
    #print(namespace, bucket, object)

    # retrieve object from object storage
    get_obj = object_storage.get_object(namespace, bucket, object)
    with open('result', 'wb') as f:
        for chunk in get_obj.data.raw.stream(1024 * 1024, decode_content=False):
            f.write(chunk)

    return send_file('result', mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
