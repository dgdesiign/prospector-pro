import re
import argparse
from src.prospector import fetch_leads, save_leads
from src.database import init_db, SessionLocal
from src.models import Lead
from src.brasil_api import consultar_cnpj_detalhado
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()

def normalize_location(cidade: str) -> str:
    if not cidade:
        return ""
    cidade = re.sub(r'\s+', ' ', cidade).strip()
    cidade = re.sub(r'\s*[-/]\s*', ', ', cidade)
    return cidade.title()

def show_leads():
    db = SessionLocal()
    leads = db.query(Lead).order_by(Lead.tier.asc(), Lead.rating.desc()).limit(50).all()
    db.close()
    if not leads:
        console.print("[yellow]Nenhum lead encontrado no banco.[/yellow]")
        return
    table = Table(title="Leads Prospectados")
    table.add_column("ID", justify="right")
    table.add_column("Nome")
    table.add_column("Telefone")
    for lead in leads:
        table.add_row(str(lead.id), lead.nome, lead.telefone or "-")
    console.print(table)

async def search_flow(query=None, cidade=None, max_r=None):
    if not query:
        query = Prompt.ask("O que você busca? (ex: Restaurantes)")
    if cidade is None:
        cidade = Prompt.ask("Em qual cidade? (ex: Salvador, BA)", default="")
    if not max_r:
        max_r = int(Prompt.ask("Quantidade máxima", default="10"))
    
    cidade_clean = normalize_location(cidade)
    try:
        leads = await fetch_leads(query, cidade_clean, max_r)
        if leads:
            save_leads(leads)
            console.print(f"[green]Sucesso! {len(leads)} leads processados.[/green]")
    except Exception as e:
        console.print(f"[red]Erro na busca: {e}[/red]")

async def investigar_cnpj():
    cnpj = Prompt.ask("\n[bold yellow]Digite o CNPJ para investigação profunda[/bold yellow]")
    with console.status("[bold green]Acessando base da Receita Federal..."):
        dados = await consultar_cnpj_detalhado(cnpj)
    
    if not dados:
        console.print("[red]Empresa não encontrada ou erro na API.[/red]")
        return

    # Painel de Informações Básicas
    info_basica = (
        f"[bold]Razão Social:[/bold] {dados['razao_social']}\n"
        f"[bold]Nome Fantasia:[/bold] {dados['nome_fantasia'] or '---'}\n"
        f"[bold]CNPJ:[/bold] {dados['cnpj']} ({'MATRIZ' if dados['is_matriz'] else 'FILIAL'})\n"
        f"[bold]Capital Social:[/bold] R$ {dados['capital_social']:,.2f}\n"
        f"[bold]Atividade:[/bold] {dados['atividade_principal']}"
    )
    console.print(Panel(info_basica, title="Dados Oficiais", border_style="blue"))

    # Painel de Contato (Inteligência Sênior)
    contato = (
        f"[bold]Telefone:[/bold] {dados['telefone']}\n"
        f"[bold]Email Oficial:[/bold] [green]{dados['email_oficial'] or 'NÃO ENCONTRADO'}[/green]\n"
        f"[bold]Email Contabilidade:[/bold] [yellow]{dados['email_contabilidade'] or '---'}[/yellow]\n"
        f"[bold]Endereço:[/bold] {dados['endereco']}"
    )
    console.print(Panel(contato, title="Inteligência de Contato", border_style="green"))

    # Tabela de Sócios
    if dados['socios']:
        table = Table(title="Tomadores de Decisão (Sócios/Diretores)")
        table.add_column("Nome", style="white", bold=True)
        table.add_column("Cargo", style="cyan")
        for socio in dados['socios']:
            table.add_row(socio['nome'], socio['cargo'])
        console.print(table)

    # NOVO: Gerar Dossiê de Guerra e Site Proposta
    if Prompt.confirm("\n[bold magenta]Deseja gerar a Proposta Premium (Site HTML) para este lead?[/bold magenta]"):
        from src.intelligence import SalesBrain
        dossie = SalesBrain.gerar_dossie_guerra(dados)
        html_content = SalesBrain.gerar_site_proposta(dossie)
        
        file_name = f"proposta_{dados['cnpj']}.html"
        with open(file_name, "w") as f:
            f.write(html_content)
        
        console.print(f"[green]✅ Proposta Premium gerada: {file_name}[/green]")
        console.print("[yellow]Envie este arquivo ou suba o HTML para o seu servidor para impressionar o cliente.[/yellow]")

async def main():
    init_db()
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnpj", help="CNPJ para investigar")
    args = parser.parse_args()

    if args.cnpj:
        await investigar_cnpj_direto(args.cnpj)
        return

    while True:
        console.print("\n[bold cyan] Prospector Pro v2.0 - Sênior Mode [/bold cyan]")
        console.print("1. Buscar novos leads (Google Maps Mode)")
        console.print("2. [bold magenta]Investigação Profunda (CNPJ/Receita)[/bold magenta]")
        console.print("3. Ver leads salvos")
        console.print("4. [bold green]Gerar Roteiro de Webinar (Escala)[/bold green]")
        console.print("5. [bold yellow]Auditoria de Equipe (Governança)[/bold yellow]")
        console.print("6. [bold blue]Gerar Master Blueprint RevOps (A a Z)[/bold blue]")
        console.print("7. Sair")
        
        op = Prompt.ask("Escolha uma opção", choices=["1", "2", "3", "4", "5", "6", "7"])
        
        if op == "1":
            await search_flow()
        elif op == "2":
            await investigar_cnpj()
        elif op == "3":
            show_leads()
        elif op == "4":
            gerar_webinar()
        elif op == "5":
            auditar_equipe()
        elif op == "6":
            gerar_blueprint()
        elif op == "7":
            break

def gerar_blueprint():
    empresa = Prompt.ask("Qual é o nome da empresa do seu cliente?")
    faturamento = float(Prompt.ask("Qual é o faturamento atual estimado da empresa? (ex: 50000)", default="50000"))
    ticket = float(Prompt.ask("Qual é o Ticket Médio das vendas dele? (ex: 5000)", default="5000"))
    
    from src.intelligence import SalesBrain
    md_content = SalesBrain.gerar_funil_revops_completo(empresa, faturamento, ticket)
    file_name = f"blueprint_{empresa.replace(' ', '_').lower()}.md"
    with open(file_name, "w") as f:
        f.write(md_content)
    console.print(f"[green]✅ Master Blueprint RevOps gerado: {file_name}[/green]")
    console.print("[yellow]Envie este projeto completo de ponta a ponta para fechar contratos de R$ 15k a R$ 36k.[/yellow]")


def gerar_webinar():
    nicho = Prompt.ask("Qual é o nicho de mercado? (ex: Energia Solar, Clínicas)")
    perda = float(Prompt.ask("Qual a perda mensal estimada média do setor? (ex: 15000)", default="15000"))
    from src.intelligence import SalesBrain
    md_content = SalesBrain.gerar_roteiro_webinar(nicho, perda)
    file_name = f"webinar_{nicho.replace(' ', '_').lower()}.md"
    with open(file_name, "w") as f:
        f.write(md_content)
    console.print(f"[green]✅ Roteiro de Webinar gerado: {file_name}[/green]")

def auditar_equipe():
    db = SessionLocal()
    leads = db.query(Lead).all()
    db.close()
    
    leads_data = []
    for lead in leads:
        # Simulamos que leads sem 'rating' não tiveram o Impacto (I) quantificado
        has_impact = bool(lead.rating and lead.rating > 0)
        leads_data.append({"id": lead.id, "impacto_financeiro": has_impact})
        
    from src.intelligence import SalesBrain
    md_content = SalesBrain.gerar_auditoria_revops(leads_data)
    file_name = "auditoria_revops.md"
    with open(file_name, "w") as f:
        f.write(md_content)
    console.print(Panel(md_content, title="Auditoria Realizada", border_style="yellow"))
    console.print(f"[green]✅ Relatório de Governança gerado: {file_name}[/green]")

async def investigar_cnpj_direto(cnpj):
    # Versão não interativa para testes rápidos
    dados = await consultar_cnpj_detalhado(cnpj)
    if dados:
        socios_nomes = [s['nome'] for s in dados['socios']]
        print(f"Empresa: {dados['razao_social']} | Sócios: {socios_nomes}")
