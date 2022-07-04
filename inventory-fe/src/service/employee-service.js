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

// get list of Employees
const getEmployeesList = () =>
  axios
    .get(`/employees/${getUser()}`, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    })
    .then((response) => response.data);

// Create Employee
const createEmployee = (employee) =>
  axios
    .post(`/employee/${getUser()}`, employee, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    })
    .then((response) => response.data);

// Update Employee
const updateEmployee = (employee) =>
  axios.put(`/employee/${getUser()}/${employee.id}/update`, employee, {
    headers: {
      Authorization: `Bearer ${getToken()}`,
    },
  });

// Delete Employee
const deleteEmployee = (employeeId) =>
  axios
    .delete(`/employee/${getUser()}/${employeeId}/delete`, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    })
    .then((response) => response.data);

// export functions
export const employeeServices = {
  getEmployeesList,
  createEmployee,
  updateEmployee,
  deleteEmployee,
};
