import datetime
import json
import os
import sys
from random import randint

import discord
from discord.ext import commands
from web3 import Web3
from cryptoaddress import EthereumAddress

from utils.db import Database

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


def has_roles(context):
    roles = [role.id for role in context.message.author.roles]
    for id in config["admin_role_id"]:
        if id in roles:
            return True
    return False


db = Database()


class Eth(commands.Cog, name="eth"):
    def __init__(self, bot):
        self.bot = bot

    def validate_address(self, address):
        if self.verify_address(address):
            try:
                address = EthereumAddress(self.parse_address(address))
                return address
            except ValueError:
                return False

    @staticmethod
    def parse_address(address):
        return Web3.toChecksumAddress(address)

    @staticmethod
    def verify_address(address):
        return Web3.isAddress(address)

    @commands.command(name="peek",
                      description=f"Check the ETH wallet associated with an account. Syntax: '!peek @user'")
    async def peek(self, context, member: discord.Member):
        # if has_roles(context):
        if db.check_if_exists(member.id):
            address = db.get_address(member.id)
            embed = discord.Embed(color=randint(0, 0x000ff),
                                  description=f"**The ETH wallet of {member.mention} is** `{address}`")

            embed.set_thumbnail(url=member.avatar_url)
            embed.timestamp = datetime.datetime.now()
            await context.reply(embed=embed)
        else:
            embed = discord.Embed(color=0x000ff,
                                  description=f"**{member.mention} hasn't set their ETH wallet yet!**")
            embed.timestamp = datetime.datetime.now()
            await context.reply(embed=embed)

    @commands.command(name="verify",
                      description=f"Verify the ETH wallet associated with your account. If verified successfully, it will be added to the database. Syntax: '!verify <address>'")
    async def verify_address(self, context, address: str):
        address = self.validate_address(address.rstrip())
        if address:
            if not db.check_if_exists(context.author.id):
                db.add_address(context.author.id, address)
                embed = discord.Embed(color=randint(0, 0x000ff),
                                      description="**ETH wallet added successfully in the database!**")
                embed.timestamp = datetime.datetime.now()
                await context.reply(embed=embed)
            else:
                embed = discord.Embed(color=0x000ff,
                                      description=f"**{context.author.mention} You have already set your ETH wallet."
                                                  f" If you wish to update your address,"
                                                  f" please use the `!update <address>` command.**")
                embed.timestamp = datetime.datetime.now()
                await context.reply(embed=embed)
        else:
            embed = discord.Embed(color=0x000ff,
                                  description=f"**{context.author.mention} Your ETH wallet was not verified."
                                              f" Please try again.**")
            embed.timestamp = datetime.datetime.now()
            await context.reply(embed=embed)

    @commands.command(name="remove",
                      description=f"Remove the ETH wallet associated with your account. Syntax: '!remove'")
    async def remove_address(self, context):
        if db.check_if_exists(context.author.id):
            db.remove_address(context.author.id)
            embed = discord.Embed(color=randint(0, 0x000ff),
                                  description="**ETH wallet associated with your account was removed successfully!**")
            embed.timestamp = datetime.datetime.now()
            await context.reply(embed=embed)
        else:
            embed = discord.Embed(color=0x000ff,
                                  description=f"**{context.author.mention} Your wallet doesn't exist in the database"
                                              f" or it has already been removed!**")
            embed.timestamp = datetime.datetime.now()
            await context.reply(embed=embed)

    @commands.command(name="update",
                      description=f"Update the ETH wallet associated with your account. Syntax: '!update <address>'")
    async def update_address(self, context, address):
        address = self.validate_address(address.rstrip())
        if address:
            if db.check_if_exists(context.author.id):
                db.update_address(context.author.id, address)
                embed = discord.Embed(color=randint(0, 0x000ff),
                                      description="**ETH wallet updated successfully in the database!**")
                embed.timestamp = datetime.datetime.now()
                await context.reply(embed=embed)
            else:
                embed = discord.Embed(color=0x000ff,
                                      description=f"**{context.author.mention} You have not set your ETH wallet."
                                                  f" If you wish to add your wallet,"
                                                  f" please use the `!set <address>` command.**")
               embed.timestamp = datetime.datetime.now()
                await context.reply(embed=embed)
        else:
            embed = discord.Embed(color=0x000ff,
                                  description=f"**{context.author.mention} You did not provide a valid ETH wallet."
                                              f" Please try again.**")
            embed.timestamp = datetime.datetime.now()
            await context.reply(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, (commands.CommandNotFound, discord.HTTPException)):
            return

        if isinstance(error, commands.MissingPermissions):
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description="You don't have the permission to use this command."))
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description=f"You forgot to provide an argument, please do it like: `{ctx.command.name} {ctx.command.usage}`"))


def setup(bot):
    bot.add_cog(Eth(bot))
