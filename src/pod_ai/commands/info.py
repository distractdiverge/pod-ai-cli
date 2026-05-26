import typer
from pathlib import Path
import json

from pod_ai.reader import read_project
from pod_ai.models import ProjectInfo
from pod_ai.utils import java_date_to_iso

app = typer.Typer()


@app.command()
def info(
    file: str = typer.Argument(..., help="Path to .pod or .xml file"),
):
    """Display project metadata as JSON."""
    file_path = Path(file)
    if not file_path.exists():
        error = {"error": f"File not found: {file}", "code": "FILE_NOT_FOUND"}
        typer.echo(json.dumps(error), err=True)
        raise typer.Exit(1)

    try:
        project = read_project(str(file_path))
        props = project.getProjectProperties()

        project_info = ProjectInfo(
            name=props.getProjectTitle(),
            project_id=props.getProjectID(),
            start_date=java_date_to_iso(props.getStartDate()),
            finish_date=java_date_to_iso(props.getFinishDate()),
            status_date=java_date_to_iso(props.getStatusDate()),
            author=props.getAuthor(),
            company=props.getCompany(),
            currency_symbol=props.getCurrencySymbol(),
            task_count=len(list(project.getTasks())) if project.getTasks() else 0,
            resource_count=len(list(project.getResources())) if project.getResources() else 0,
        )
        output = project_info.model_dump_json(indent=2, exclude_none=False)
        typer.echo(output)
    except FileNotFoundError as e:
        error = {"error": str(e), "code": "FILE_NOT_FOUND"}
        typer.echo(json.dumps(error), err=True)
        raise typer.Exit(1)
    except Exception as e:
        error = {"error": str(e), "code": "READ_ERROR"}
        typer.echo(json.dumps(error), err=True)
        raise typer.Exit(1)
