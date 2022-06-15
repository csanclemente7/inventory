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

// get list of items
const getItemsList = () =>
  axios
    .get(`/items/${getUser()}`, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    })
    .then((response) => response.data);

// Create item
const createItem = (item) =>
  axios
    .post(`/item/${getUser()}`, item, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    })
    .then((response) => response.data);

// Update item
const updateItem = (item) =>
  axios.put(`/item/${getUser()}/${item.id}/update`, item, {
    headers: {
      Authorization: `Bearer ${getToken()}`,
    },
  });

// Delete item
const deleteItem = (itemId) =>
  axios
    .delete(`/item/${getUser()}/${itemId}/delete`, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    })
    .then((response) => response.data);

// export functions
export const itemServices = {
  getItemsList,
  createItem,
  updateItem,
  deleteItem,
};
