import { NavLink } from "react-router-dom";

export default function Sidebar() {

    return (

        <aside className="sidebar">

            <h2>TattvaAI</h2>

            <ul>

                <li>

                    <NavLink

                        to="/"

                        className={({ isActive }) =>

                            isActive ? "active-link" : ""

                        }

                    >

                        Dashboard

                    </NavLink>

                </li>

                <li>

                    <NavLink

                        to="/investigation/1"

                        className={({ isActive }) =>

                            isActive ? "active-link" : ""

                        }

                    >

                        Investigations

                    </NavLink>

                </li>

                <li>

                    <NavLink

                        to="/history"

                        className={({ isActive }) =>

                            isActive ? "active-link" : ""

                        }

                    >

                        History

                    </NavLink>

                </li>

                <li>

                    <NavLink

                        to="/reports"

                        className={({ isActive }) =>

                            isActive ? "active-link" : ""

                        }

                    >

                        Reports

                    </NavLink>

                </li>

                <li>

                    <NavLink

                        to="/settings"

                        className={({ isActive }) =>

                            isActive ? "active-link" : ""

                        }

                    >

                        Settings

                    </NavLink>

                </li>

            </ul>

        </aside>

    );

}