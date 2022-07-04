<template>
  <div class="main">
    <section class="home" v-if="modals.home">
      <div class="home-data">
        <div class="button-container">
          <button class="button red" @click="openModal('output')">
            <img src="../assets/img/exit.png" />
          </button>

          <button class="button green" @click="openModal('input')">
            <img src="../assets/img/entry.png" alt="" />
          </button>
        </div>
        <div class="image" v-if="false">
          <img src="../assets/img/home_image.svg" alt="" />
          <h3>Todo al día</h3>
        </div>
      </div>
    </section>
    <!--- MODALS -->
    <section class="modals_container" v-if="!modals.home">
      <!-- OUTPUT MODAL -->
      <div class="modals modals_output" v-if="modals.output">
        <!--  botón cerrar -- -->
        <i
          class="fas fa-times"
          @click="openModal('home')"
          v-if="!modals.home"
        ></i>
        <!-- título -->
        <div class="modals_title">
          <h1>Salida&nbsp;</h1>
          <i class="fas fa-arrow-right"></i>
        </div>
        <form>
          <select id="select_employee" v-model="employee.name">
            <option v-for="employee in employees" :key="employee">
              {{ employee }}
            </option>
          </select>
          <button>Siguiente</button>
        </form>
      </div>
      <!-- INPUT MODAL -->
      <div class="modals modals_input" v-if="modals.input">
        <!--  botón cerrar -- -->
        <i
          class="fas fa-times"
          @click="openModal('home')"
          v-if="!modals.home"
        ></i>
        <!-- título -->
        <div class="modals_title">
          <i class="fas fa-arrow-right"></i>
          <h1>&nbsp;Entrada</h1>
        </div>
      </div>
    </section>
  </div>
</template>
<script>
import axios from "axios";
import { employeeServices } from "../service/employee-service";
export default {
  name: "Home",
  data: function () {
    return {
      modals: {
        home: true,
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
      employee: {
        name: "",
      },
      employees: [],
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

    openModal: function (modal) {
      this.modals[modal] = true;
      if (modal != "home") {
        let home = document.querySelector(".home");
        home.classList.add("parentDiv");
      }
      // iterar objeto
      for (let key in this.modals) {
        if (key != modal) {
          this.modals[key] = false;
        }
      }
    },

    getEmployees: function () {
      employeeServices.getEmployeesList().then((result) => {
        this.employees = result;
      });
    },

    closeModal: function (modal) {
      this.modals[modal] = false;
      let home = document.querySelector(".home");
      home.classList.remove("parentDiv");
    },
  },

  created: function () {
    this.verifyAuth();
    this.getEmployees();
    console.log(this.employees);
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.main {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.home {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.home-data {
  width: 100%;
}

.home-data image {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
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
@import "../assets/css/common/modals.css";
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
