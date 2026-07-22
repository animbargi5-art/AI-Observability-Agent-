import api from "../api/axios";

export const startInvestigation = async () => {

    const response = await api.post(
        "/investigation/start"
    );

    return response.data;

};

export const getAllInvestigations = async () => {

    const response = await api.get(
        "/investigation/history"
    );

    return response.data;

};

export const getInvestigationById = async (id) => {

    const response = await api.get(
        `/investigation/${id}`
    );

    return response.data;

};

export const deleteInvestigation = async (id) => {

    const response = await api.delete(
        `/investigation/${id}`
    );

    return response.data;

};