import discord
from discord import app_commands
from discord.ui import Button, View
import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Configurações do bot
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if not TOKEN:
    print("❌ ERRO: Token não encontrado!")
    print("📝 Crie um arquivo .env com DISCORD_BOT_TOKEN=seu_token_aqui")
    exit(1)

class LinkBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        
    async def setup_hook(self):
        await self.tree.sync()
        print(f'✅ Bot {self.user} está online!')

bot = LinkBot()

class LinkView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Obter Link", style=discord.ButtonStyle.primary, custom_id="get_link")
    async def get_link_button(self, interaction: discord.Interaction, button: Button):
        try:
            embed = discord.Embed(
                title="🔗 Link Disponível",
                description="Aqui está o link que você solicitado:",
                color=0x00ff00
            )
            embed.add_field(
                name="Link de Acesso",
                value="https://exemplo.com/seu-link-aqui",
                inline=False
            )
            
            await interaction.user.send(embed=embed)
            await interaction.response.send_message("📬 Link enviado na sua DM!", ephemeral=True)
            
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Não consigo enviar mensagens na sua DM! Por favor, habilite as mensagens diretas.",
                ephemeral=True
            )

class CopyView(View):
    def __init__(self, link):
        super().__init__(timeout=300)
        self.link = link
    
    @discord.ui.button(label="📋 Copiar Link", style=discord.ButtonStyle.secondary)
    async def copy_link(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(
            f"🔗 **Link para copiar:** ```{self.link}```",
            ephemeral=True
        )

@bot.event
async def on_ready():
    print(f'🎯 Bot conectado como {bot.user}')
    print('💡 Use o comando /setup no seu servidor')

@bot.tree.command(name="setup", description="Configura o bot de links")
async def setup(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🔗 Obter Link",
        description="Clique no botão abaixo para receber o link na sua DM",
        color=0x5865F2
    )
    embed.add_field(
        name="Como usar",
        value="1. Clique em **Obter Link**\n2. Verifique suas mensagens diretas\n3. Use o link copiável",
        inline=False
    )
    
    view = LinkView()
    await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name="link", description="Recebe o link diretamente")
async def link_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🔗 Seu Link",
        description="Aqui está o link solicitado:",
        color=0x00ff00
    )
    embed.add_field(
        name="Link de Acesso",
        value="https://discord.gg/mth48KhNWn",
        inline=False
    )
    
    try:
        copy_view = CopyView("https://exemplo.com/seu-link-aqui")
        await interaction.user.send(embed=embed, view=copy_view)
        await interaction.response.send_message("📬 Link enviado na sua DM!", ephemeral=True)
    except discord.Forbidden:
        copy_view = CopyView("https://exemplo.com/seu-link-aqui")
        await interaction.response.send_message(embed=embed, view=copy_view, ephemeral=True)

@bot.tree.command(name="setlink", description="Define um novo link (apenas admins)")
@app_commands.default_permissions(administrator=True)
async def set_link(interaction: discord.Interaction, novo_link: str):
    await interaction.response.send_message(
        f"✅ Link atualizado para: {novo_link}",
        ephemeral=True
    )

if __name__ == "__main__":
    print("🚀 Iniciando bot Discord...")
    print("📁 Lendo configurações do arquivo .env")
    bot.run(TOKEN)
