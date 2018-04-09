from flask import Flask, jsonify, request
import stream

app = Flask(__name__)

# Instantiate new client
client = stream.connect('zhzypp7eu79m' 'cs3pn895p6upexng5nr72qc7tk6jnpvgr4vpxa88haecckbekvdju7wxf6bmeqdv', location='us-east')

feed = [
    {
        'actor': 'Attila', 
        'verb': 'post',
        'object': '1', 
        'target': 'General',
        'time': '2018-03-22T20:30:45.123', 
        'foreign_id': "Attila's feed", 
        'post': 'Stevens is the best university!'
    }
]
        

# POST request
@app.route('/feed/<string:name>/<user:id>/<obj:id>', methods=['POST']) #receive a post
def create_post(name):
    request_data = request.get_json()
    attila = client.feed('user', 'Attila')
    # add an activity
    new_post = attila.add_activity(
    {'actor': request_data['actor'], 
    'verb': request_data['verb'], 
    'object': request_data['object'], 
    'target': request_data['target'], 
    'time': request_data['time'], 
    'foreign_id': request_data['foreign_id'], 
    'post': request_data['post']}) 
    
    feed.append(new_post)
    return jsonify(new_post)
  
# GET request      
@app.route('/feed') #send a post
def display_post():
    return jsonify({'feed': feed})
    
  
if __name__ == '__main__':  
    app.run(debug=True)