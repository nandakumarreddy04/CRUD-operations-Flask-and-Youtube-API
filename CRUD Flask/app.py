from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/videos_db"
mongo = PyMongo(app)

# Create a new video
@app.route('/videos', methods=['POST'])
def create_video():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    views = data.get('views')

    if name and description and views:
        video_id = mongo.db.videos.insert_one({
            'name': name,
            'description': description,
            'views': views
        })
        return jsonify(str(video_id.inserted_id)), 201
    else:
        return jsonify({'error': 'Missing data fields'}), 400

# Retrieve all videos
@app.route('/videos', methods=['GET'])
def get_all_videos():
    videos = mongo.db.videos.find()
    video_list = []
    for video in videos:
        video['_id'] = str(video['_id'])
        video_list.append(video)
    return jsonify(video_list), 200

# Retrieve a specific video by ID
@app.route('/videos/<string:video_id>', methods=['GET'])
def get_video(video_id):
    video = mongo.db.videos.find_one({'_id': ObjectId(video_id)})
    if video:
        video['_id'] = str(video['_id'])
        return jsonify(video), 200
    else:
        return jsonify({'error': 'Video not found'}), 404

# Update a video
@app.route('/videos/<string:video_id>', methods=['PUT'])
def update_video(video_id):
    data = request.json
    name = data.get('name')
    description = data.get('description')

    if name and description:
        result = mongo.db.videos.update_one({'_id': ObjectId(video_id)},
                                            {'$set': {'name': name, 'description': description}})
        if result.modified_count == 1:
            return jsonify({'message': 'Video updated successfully'}), 200
        else:
            return jsonify({'error': 'Video not found'}), 404
    else:
        return jsonify({'error': 'Missing data fields'}), 400

# Delete a video
@app.route('/videos/<string:video_id>', methods=['DELETE'])
def delete_video(video_id):
    result = mongo.db.videos.delete_one({'_id': ObjectId(video_id)})
    if result.deleted_count == 1:
        return jsonify({'message': 'Video deleted successfully'}), 200
    else:
        return jsonify({'error': 'Video not found'}), 404
    

# Get a video by ID and increment its view count by 1
@app.route('/videos/<string:video_id>', methods=['GET'])
def getincrement_video(video_id):
    try:
        # Find the video in the database
        video = mongo.db.videos.find_one({'_id': ObjectId(video_id)})
        if video:
            # Increment the view count
            views = video.get('views', 0) + 1
            # Update the view count in the database
            result = mongo.db.videos.update_one({'_id': ObjectId(video_id)},
                                                 {'$set': {'views': views}})
            if result.modified_count == 1:
                # Return the video data with the updated view count
                return jsonify({
                    'name': video.get('name'),
                    'description': video.get('description'),
                    'views': views
                }), 200
            else:
                return jsonify({'error': 'Failed to update view count'}), 500
        else:
            return jsonify({'error': 'Video not found'}), 404
    except Exception as e:
        print("Error getting video:", str(e))
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(port=3000,debug=True)
