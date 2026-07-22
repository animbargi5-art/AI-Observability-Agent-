import "../../styles/action-panel.css";

export default function ActionPanel({

    onRefresh,

    onDelete

}) {

    return (

        <div className="action-panel">

            <h2>

                Investigation Actions

            </h2>

            <div className="action-buttons">

                <button

                    className="refresh-btn"

                    onClick={onRefresh}

                >

                    Refresh

                </button>

                <button

                    className="delete-btn"

                    onClick={onDelete}

                >

                    Delete Investigation

                </button>

            </div>

        </div>

    );

}