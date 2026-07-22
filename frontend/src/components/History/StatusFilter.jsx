import "../../styles/status-filter.css";

export default function StatusFilter({

    value,

    onChange

}) {

    return (

        <div className="status-filter">

            <label>

                Status

            </label>

            <select

                value={value}

                onChange={(event) =>

                    onChange(event.target.value)

                }

            >

                <option value="ALL">

                    All

                </option>

                <option value="INVESTIGATING">

                    INVESTIGATING

                </option>

                <option value="NO_ISSUE">

                    NO_ISSUE

                </option>

                <option value="RESOLVED">

                    RESOLVED

                </option>

                <option value="FAILED">

                    FAILED

                </option>

            </select>

        </div>

    );

}