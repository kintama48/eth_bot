const mongoose = require('mongoose');
//const url = `mongodb+srv://roz:pass@roz.pbrfu.mongodb.net/Roz?retryWrites=true&w=majority`
//const url = `mongodb://localhost:27017`
const url = `mongodb+srv://eth_bot:eth_pass@cluster0.rertq.mongodb.net/eth_records?retryWrites=true&w=majority`


async function main() {
    await mongoose.connect(url).then((res, err) => {
        if(res){
            console.log("Database connected!")
        } else {
            console.log("Database connection failed")
        }
    }
    )
}

main();