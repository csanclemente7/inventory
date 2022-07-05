import axios from "axios";
import jwt_decode from "jwt-decode";

// url base
axios.defaults.baseURL = "https://inventory-bk.herokuapp.com";

// getToken
const getToken = () => {
  let token = localStorage.getItem("token_access");
  return token;
};
const getUser = () => {
  return jwt_decode(getToken()).user_id.toString();
};

// get list of reports status output
const getReportsOutputList = () =>
  axios
    .get(`/reports/${getUser()}/outside`, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    })
    .then((response) => response.data);

// get list of reports
const getReportsList = () =>
  axios
    .get(`/reports/${getUser()}`, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    })
    .then((response) => response.data);

// Create report
const createReport = (report) =>
  axios
    .post(`/report/${getUser()}`, report, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    })
    .then((response) => response.data);

// Update report
const updateReport = (report) =>
  axios.put(`/report/${getUser()}/${report.id}/update`, report, {
    headers: {
      Authorization: `Bearer ${getToken()}`,
    },
  });

// Delete item
const deleteReport = (reportId) =>
  axios
    .delete(`/report/${getUser()}/${reportId}/delete`, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    })
    .then((response) => response.data);

// export functions
export const reportServices = {
  getReportsOutputList,
  getReportsList,
  createReport,
  updateReport,
  deleteReport,
};
