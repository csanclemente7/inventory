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
      <!-- INSUMOS MODAL -->
      <div class="modals modals_insumos" v-if="modals.insumos">
        <!--  botón cerrar -- -->
        <i
          class="fas fa-times"
          @click="openModal('home')"
          v-if="!modals.home"
        ></i>
        <!-- título -->
        <div class="modals_title">
          <i class="fas fa-cubes fa-2x"></i>
          <h1>&nbsp;Insumos</h1>
        </div>

        <!-- TABLA INSUMOS -->
        <!--         <table class="custom-responsiva">
          <thead>
            <tr>
              <th>#</th>
              <th>Fecha</th>
              <th>Cliente</th>
              <th>Valor</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="quotation in paginatedData"
              :key="quotation"
              id="table_row"
              v-on:click="
                openPopUpUpdateQuotation('updateQuotation', quotation)
              "
            >
              <td>{{ quotation.id }}</td>
              <td>{{ quotation.date }}</td>
              <td>{{ quotation.client_name }}</td>
              <td>${{ priceToString(quotation.total) }}</td>
            </tr>
          </tbody>
        </table>
        <div class="pagination-container" v-if="!startLoader">
          <nav aria-label="Page navigation example">
            <ul class="pagination">
              <li class="page-item">
                <a class="page-link" v-on:click="getPreviousPage()">Anterior</a>
              </li>
              <li
                v-for="page in pagination.totalPages(quotations.length)"
                :key="page"
                v-on:click="getDataPage(page, quotations)"
                class="page-item"
              >
                <a class="page-link" v-if="page != actualPage">{{ page }}</a>
                <div class="page-item active" aria-current="page">
                  <span class="page-link" v-if="page === actualPage">{{
                    actualPage
                  }}</span>
                </div>
              </li>

              <li class="page-item">
                <a class="page-link" v-on:click="getNextPage()">Siguiente</a>
              </li>
            </ul>
          </nav>
        </div> -->
      </div>
    </section>
    <div class="float-buttons-container">
      <button class="button create-item-btn" @click="openModal('insumos')">
        INSUMOS
      </button>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import { itemServices } from "../service/item-service";
import { paginationItems } from "../paginationItems";
import { employeeServices } from "../service/employee-service";
export default {
  name: "Home",
  data: function () {
    return {
      items: [],

      paginationItems: paginationItems,
      paginatedDataItems: [],
      actualPageItems: 1,
      startLoader: false,

      modals: {
        home: true,
        output: false,
        input: false,
        item: false,
        /* insumos: false, */
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

    // PAGINATION FUNCTIONS
    // trae los datos paginados de items
    getDataPageItems: function (page, items) {
      this.filterSearch = ""; // borra el filtro
      this.actualPageItems = page;
      this.paginatedDataItems = paginationItems.getDataPage(page, items);
    },

    // trae los datos de la página anterior
    getPreviousPageItems: function () {
      this.filterSearch = ""; // borra el filtro
      this.actualPageItems = paginationItems.getPreviousPage(
        this.actualPageItems
      );

      this.paginatedDataItems = paginationItems.getDataPage(
        this.actualPageItems,
        this.items
      );
    },

    // trae los datos de la página siguiente
    getNextPageItems: function () {
      this.filterSearch = ""; // borra el filtro
      this.actualPageItems = paginationItems.getNextPage(
        this.actualPageItems,
        paginationItems.totalPages(this.items.length)
      );

      this.paginatedDataItems = paginationItems.getDataPage(
        this.actualPageItems,
        this.items
      );
    },
    getInitialData: function () {
      itemServices.getItemsList().then((result) => {
        this.items = result;
        this.totalInitialDataResults += 1;
        this.paginatedDataItems = paginationItems.getDataPage(
          this.actualPageItems,
          this.items
        );
      });
    },
  },
  created: function () {
    this.verifyAuth();
    this.getInitialData();
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
@import "../assets/css/common/float-buttons.css";
@import "../assets/css/common/links.css";
@import "../assets/css/common/suggestion.css";
@import "../assets/css/base/base.css";
@import "../assets/css/common/table.css";
@import "../assets/css/common/tableResults.css";
@import "../assets/css/common/lds-ripple.css";
</style>
