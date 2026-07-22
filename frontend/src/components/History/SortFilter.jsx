import "../../styles/sort-filter.css";

export default function SortFilter({

    value,

    onChange

}) {

    return (

        <div className="sort-filter">

            <label>

                Sort By

            </label>

            <select

                value={value}

                onChange={(event) =>

                    onChange(event.target.value)

                }

            >

                <option value="NEWEST">

                    Newest First

                </option>

                <option value="OLDEST">

                    Oldest First

                </option>

                <option value="CONFIDENCE_HIGH">

                    Highest Confidence

                </option>

                <option value="CONFIDENCE_LOW">

                    Lowest Confidence

                </option>

            </select>

        </div>

    );

}