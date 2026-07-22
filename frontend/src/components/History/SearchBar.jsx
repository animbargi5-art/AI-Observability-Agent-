import "../../styles/search-bar.css";

export default function SearchBar({

    value,

    onChange

}) {

    return (

        <input

            type="text"

            placeholder="Search investigations..."

            value={value}

            onChange={(event) =>

                onChange(event.target.value)

            }

            className="search-bar"

        />

    );

}