<template>
  <div class="home">
    <div class="home-data">
      <div class="button-container">
        <button v-on:click="openPopUp('output')" class="button red">
          <img src="../assets/img/exit.png" />
        </button>

        <button v-on:click="openPopUp('input')" class="button green">
          <img src="../assets/img/entry.png" alt="" />
        </button>
      </div>
      <div class="image" v-if="false">
        <img src="../assets/img/home_image.svg" alt="" />
        <h3>Todo al día</h3>
      </div>
    </div>
  </div>
  <!--- POP UP OUTPUTS -->
  <section class="popups_container">
    <div class="popup pop-output" v-if="popUps.output">
      <div class="popup-close-container">
        <div class="popup_close" v-on:click="closePopUp('output')">
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
      <div class="popup-title rd"><h1>Salida</h1></div>

      <!-- FORM OUTPUT -->
      <form
        class="formulario output-form"
        v-on:submit.prevent="processCreateItem"
      >
        <div class="input-container">
          <input
            type="text"
            name=""
            id=""
            class="input input-salida"
            placeholder="Empleado"
            v-model="outputReport.employee"
          />
        </div>
        <div class="input-container">
          <input
            type="text"
            name=""
            id=""
            class="input input-salida"
            placeholder="Código Item"
            v-model="outputReport.item"
          />
          &nbsp;
          <i class="fas fa-plus"></i>
        </div>
        <p>Observaciones (opcional)</p>
        <div class="textarea-container">
          <textarea
            class="textarea"
            rows="1"
            data-min-rows="2"
            v-model="outputReport.observation"
            placeholder="Observaciones"
          ></textarea>
        </div>

        <div class="input-container">
          <button class="button submit" type="submit">
            <i class="fas fa-download"></i>
            &nbsp;Generar
          </button>
        </div>
      </form>
    </div>
    <div class="popup pop-input" v-if="popUps.input">
      <div class="popup-close-container">
        <div class="popup_close" v-on:click="closePopUp('input')">
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
      <div class="popup-title rd"><h1>Entrada</h1></div>
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
        output: false,
        input: false,
        item: false,
      },
      outputReport: {
        item: "",
        status: "output",
        observation: "",
        employee: "",
      },
      inputReport: {
        item: "",
        status: "input",
        observation: "",
        employee: "",
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
      let home = document.querySelector(".home");
      home.classList.add("parentDiv");
    },

    closePopUp: function (popUp) {
      this.popUps[popUp] = false;
      let home = document.querySelector(".home");
      home.classList.remove("parentDiv");
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
