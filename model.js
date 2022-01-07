const { Pool } = require('pg');

const connectionString = 'postgres://hamzaasaad:@localhost:5432/hamzaasaad'

let pool = new Pool({
    user: "postgres",
    host: "localhost",
    database: "postgres",
    password: "test",
    port: 5432,
})
pool.connect();
/*
pool.query('SELECT NOW()', (err, res) => {
    if(err){
        console.log('Database connection failed',err);
    }
    else {
        console.log('Database connected!');
    }
});*/

async function checkAddressExists(address){
    const select = `
        SELECT * FROM "discord" where address= $1
    `;
    const vals=[address]
    const result = await pool.query(select,vals);
    return result.rows;

}
 
module.exports ={
    connectDiscordID: async function (discordID, address){
        const isAccountConnected = await checkAddressExists(address)
        console.log(isAccountConnected)
        if (!isAccountConnected.length){
            const insert = `INSERT INTO "discord" (discord_id, address) VALUES ($1,$2);`
            const values = [discordID,address]
            
            const result = await pool.query(insert, values)
            console.log(result)
            return true
        } else {
            console.log(isAccountConnected[0].discord_id)
            return isAccountConnected[0].discord_id
        }
    }
}

/*
user: "bpksohjnqxghia",
  host: "ec2-34-230-133-163.compute-1.amazonaws.com",
  database: "d91ok380e2boea",
  password: "391cebb8cfc0080ac7f81493ebfa4e6b3b60e081da74b792ef0f9f1e0455a578",
  port: 5432,*/