import "../../styles/investigation-actions.css";

export default function InvestigationActions({

    onRefresh,

    onDelete,

    onRerun

}) {

    return (

        <div className="investigation-actions">

            <button

                onClick={onRefresh}

            >

                Refresh

            </button>

            <button

                onClick={onRerun}

            >

                Re-run Investigation

            </button>

            <button

                onClick={onDelete}

            >

                Delete Investigation

            </button>

        </div>

    );

}