import { useMemo } from "react";

import {
    ReactFlow,
    Background,
    Controls,
    MiniMap
} from "reactflow";

import "reactflow/dist/style.css";
import "../../styles/investigation-graph.css";

export default function InvestigationGraph({ investigation }) {

    if (!investigation) {

        return null;

    }

    const graph = investigation.report?.graph || {};

    const nodes = useMemo(() => {

        return (graph.nodes || []).map((node) => ({

            id: String(node.id),

            data: {
                label: node.label
            },

            position: {
                x: Math.random() * 600,
                y: Math.random() * 500
            }

        }));

    }, [graph]);

    const edges = useMemo(() => {

        return (graph.edges || []).map((edge, index) => ({

            id: `edge-${index}`,

            source: String(edge.source),

            target: String(edge.target),

            label: edge.relation,

            animated: true

        }));

    }, [graph]);

    return (

        <div className="graph-panel">

            <h2>Knowledge Graph</h2>

            <div className="graph-container">

                <ReactFlow
                    nodes={nodes}
                    edges={edges}
                    fitView
                >

                    <MiniMap />

                    <Controls />

                    <Background />

                </ReactFlow>

            </div>

        </div>

    );

}