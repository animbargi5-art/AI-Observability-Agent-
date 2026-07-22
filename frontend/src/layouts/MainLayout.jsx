import Sidebar from "../components/Sidebar/Sidebar";
import Navbar from "../components/Navbar/Navbar";

import "../styles/sidebar.css";
import "../styles/navbar.css";

export default function MainLayout({ children }) {

    return (

        <>

            <Sidebar />

            <div
                style={{
                    marginLeft: "260px",
                    minHeight: "100vh",
                    backgroundColor: "#f5f7fb"
                }}
            >

                <Navbar />

                <main
                    style={{
                        padding: "30px"
                    }}
                >

                    {children}

                </main>

            </div>

        </>

    );

}