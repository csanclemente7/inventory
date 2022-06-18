<template>
  <div class="home">
    <div class="home-data">
      <div class="button-container">
        <button v-on:click="openPopUp('exit')" class="button red">
          <img src="../assets/img/exit.png" />
        </button>

        <button v-on:click="openPopUp('entry')" class="button green">
          <img src="../assets/img/entry.png" alt="" />
        </button>
      </div>
      <div class="image">
        <img src="../assets/img/home_image.svg" alt="" />
        <h3>Todo al día</h3>
      </div>
    </div>
  </div>
  <!--- POP UP EXIT -->
  <section class="popups_container">
    <div class="popup" v-if="popUps.exit">
      <div class="popup-close-container">
        <div class="popup_close" v-on:click="closePopUp('exit')">
          <svg
            width="25"
            height="25"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            stroke="var(--link-red-light)"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
            viewBox="0 0 24 24"
          >
            <path
              d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
            />
          </svg>
        </div>
      </div>
      <div class="popup-title rd">Salida</div>

      <div class="grid-container-menu">
        <div class="input-container grid-menu-search">
          <!-- SECTION SEARCH FILTER -->
          <form>
            <input
              type="search"
              placeholder="Buscar..."
              id="input_search"
              v-model="filterSearch"
              v-on:input="filterBySearchInput"
              autocomplete="off"
            />
            <button
              type="button"
              aria-label="submit form"
              v-on:click="filterBySearchInput"
            >
              <li class="fas fa-search"></li>
            </button>
          </form>
        </div>
      </div>
      <!--  EXIT TABLE -->
      <table class="custom-responsiva">
        <thead>
          <tr>
            <th>Codigo</th>
            <th>Item</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="quotation in paginatedData"
            :key="quotation"
            id="table_row"
            v-on:click="openPopUpUpdateQuotation('updateQuotation', quotation)"
          >
            <td>{{ quotation.id }}</td>
            <td>{{ quotation.date }}</td>
            <td>{{ quotation.client_name }}</td>
            <td>${{ priceToString(quotation.total) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="popup" v-if="popUps.entry">
      <div class="popup-close-container">
        <div class="popup_close" v-on:click="closePopUp('entry')">
          <svg
            width="25"
            height="25"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            stroke="var(--link-red-light)"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
            viewBox="0 0 24 24"
          >
            <path
              d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
            />
          </svg>
        </div>
      </div>
    </div>
  </section>
</template>
<script>
import axios from "axios";
export default {
  name: "Home",
  data: function () {
    return {
      popUps: {
        exit: false,
        entry: false,
        item: false,
      },
    };
  },
  methods: {
    verifyAuth: function () {
      this.is_auth = localStorage.getItem("isAuth") || false;
      if (this.is_auth == false) {
        this.$router.push("logIn");
      }
    },

    verifyToken: function () {
      this.startLoader = true;
      return axios
        .post(
          "https://inventory-be.herokuapp.com/refresh",
          { refresh: localStorage.getItem("token_refresh") },
          { headers: {} }
        )
        .then((result) => {
          localStorage.setItem("token_access", result.data.access);
          this.startLoader = false;
        })
        .catch(() => {
          this.$emit("logOut");
        });
    },

    openPopUp: function (popUp) {
      this.popUps[popUp] = true;
    },

    closePopUp: function (popUp) {
      this.popUps[popUp] = false;
    },

    created: function () {
      this.verifyAuth();
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.home-data image {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.image img {
  width: 30%;
  height: auto;
}

h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
@import "../assets/css/common/popUp.css";
@import "../assets/css/common/grid-menu.css";
@import "../assets/css/common/inputs.css";
@import "../assets/css/common/button.css";
@import "../assets/css/common/links.css";
@import "../assets/css/common/suggestion.css";
@import "../assets/css/base/base.css";
@import "../assets/css/common/table.css";
@import "../assets/css/common/tableResults.css";
@import "../assets/css/common/lds-ripple.css";
</style>
