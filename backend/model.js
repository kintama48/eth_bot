const { Pool, Client } = require('pg');

const connectionString = 'postgres://hamzaasaad:@localhost:5432/hamzaasaad'

let pool = new Pool({
    user: "hamzaasaad",
    host: "localhost",
    database: "hamzaasaad",
    password: "",
    port: 5431,
})
pool.connect();

pool.query('SELECT NOW()', (err, res) => {
    if(err){
        console.log('Database connection failed',err);
    }
    else {
        console.log('Database connected!');
    }
});




/*
user: "bpksohjnqxghia",
  host: "ec2-34-230-133-163.compute-1.amazonaws.com",
  database: "d91ok380e2boea",
  password: "391cebb8cfc0080ac7f81493ebfa4e6b3b60e081da74b792ef0f9f1e0455a578",
  port: 5432,*/


async function checkAddressExists(discordID){
    const select = `
        SELECT * FROM users where discord_id = $1
    `;
    const vals=[discordID]
    const result = await pool.query(select,vals);
    console.log("this res",result)
    return result.rows;

}
 
module.exports ={
    connectDiscordID: async function(discordID, address){
        const isAccountConnected = await checkAddressExists(discordID)
        console.log(isAccountConnected)
        if (!isAccountConnected.length){
            const insert = `INSERT INTO public.users (discord_id, address) VALUES ($1,$2);`
            const values = [discordID,address]
            
            const result = await pool.query(insert, values)
            console.log(result)
            return true
        } 
        return false
    }
}
