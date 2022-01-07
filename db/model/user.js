const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const UserSchema = new Schema({
    discordID: {
        type: String,
        required: true
    },
    address: {
        type: String,
        required: true
    }
});

mongoose.model('User', UserSchema);