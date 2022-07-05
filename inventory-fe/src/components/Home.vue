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
        <!-- Formulario-->
        <div class="employee-form" v-if="firstPage">
          <form
            v-on:submit.prevent="
              () => {
                this.firstPage = false;
                this.secondPage = true;
              }
            "
          >
            <p>Paso 1: Selecciona trabajdores</p>
            <select
              id="select_employee"
              v-model="employee.name"
              @change="employeeSelected()"
            >
              <option v-for="employee in employees" :key="employee">
                {{ employee.name }}
              </option>
            </select>
            <p v-for="employee in employeesSelected" :key="employee">
              {{ employee }}
            </p>
            <button>Siguiente</button>
          </form>
        </div>

        <div class="search-form" v-if="secondPage">
          <form>
            <b>Empleados seleccionados</b><br />
            <br />
            <p v-for="employee in employeesSelected" :key="employee">
              {{ employee }}
            </p>
            <form v-on:submit.prevent="searchItem(item.id)">
              <input type="text" autofocus v-model="item.id" />
              <button>Agregar</button>
              <p v-for="item in itemsSelected" :key="item">{{ item }}</p>
            </form>
          </form>
          <button
            @click="
              () => {
                this.secondPage = false;
                this.firstPage = true;
              }
            "
          >
            Atras
          </button>
        </div>
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
        <div class="modal-content">
          <!-- título -->
          <div class="modals_title">
            <i class="fas fa-cubes fa-2x"></i>
            <h1>&nbsp;Insumos</h1>
          </div>
          <div class="link-container">
            <i
              class="fas fa-plus fa-2x create-item-link"
              v-if="!newItem"
              @click="newItem = !newItem"
              >&nbsp;Nuevo Item</i
            >
            <i
              class="fas fa-minus fa-2x create-item-link"
              v-if="newItem"
              @click="newItem = !newItem"
              >&nbsp;Nuevo Item</i
            >
          </div>
          <!-- CREATE ITEM FORM -->
          <form
            class="item-form"
            v-if="newItem"
            v-on:submit.prevent="processCreateItem"
          >
            <div class="item-form-title">
              <h2></h2>
            </div>
            <div class="input-container item-name">
              <input
                type="text"
                name="id"
                id="id"
                class="input"
                v-model="item.id"
                autocomplete="off"
                required
              />
              <label class="input-label" for="name">Código</label>
            </div>
            <div class="input-container item-name">
              <input
                type="text"
                name="itemName"
                id="itemName"
                class="input"
                v-model="item.name"
                autocomplete="off"
                required
              />
              <label class="input-label" for="name">Nombre</label>
            </div>
            <div class="button-container">
              <button class="button button-add-item" type="submit">
                Agregar
              </button>
            </div>
          </form>
          <br />
          <!-- UPDATE ITEM FORM -->
          <form
            class="item-form"
            v-if="updateItem"
            v-on:submit.prevent="processUpdateItem"
          >
            <div class="item-form-title">
              <h2></h2>
            </div>
            <div class="input-container item-name">
              <input
                type="text"
                name="id"
                id="id"
                class="input"
                v-model="itemUpdate.id"
                autocomplete="off"
                required
              />
              <label class="input-label" for="name">Código</label>
            </div>
            <div class="input-container item-name">
              <input
                type="text"
                name="name"
                id="name"
                class="input"
                v-model="itemUpdate.name"
                autocomplete="off"
                required
              />
              <label class="input-label" for="name">Nombre</label>
            </div>
            <div class="button-container">
              <button class="button button-add-item" type="submit">
                Actualizar
              </button>
            </div>
            <div
              class="link-container update-item-link"
              @click="updateItem = false"
            >
              Cancelar
            </div>
          </form>

          <!-- TABLA INSUMOS -->
          <table class="custom-responsiva table-items">
            <thead>
              <tr>
                <th>Código</th>
                <th>Item</th>
                <th scope="col" class="atach"></th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="item in paginatedDataItems"
                :key="item"
                id="table_row delete-custom"
                @click="
                  () => {
                    updateItem = true;
                    itemUpdate.id = item.id;
                    itemUpdate.name = item.name;
                  }
                "
              >
                <td>
                  {{ item.id }}
                </td>
                <td>
                  {{ item.name }}
                </td>
                <td>
                  <i
                    class="fas fa-trash delete-icon"
                    @click="processDeleteItem(item.id)"
                  ></i>
                </td>
              </tr>
            </tbody>
          </table>
          <br />
          <!-- PAGINATION ITEMS -->
          <div class="pagination-container">
            <nav aria-label="Page navigation example">
              <ul class="pagination">
                <li class="page-item">
                  <a class="page-link" v-on:click="getPreviousPageItems()"
                    >Anterior</a
                  >
                </li>
                <li
                  v-for="page in paginationItems.totalPages(items.length)"
                  :key="page"
                  v-on:click="getDataPageItems(page, items)"
                  class="page-item"
                >
                  <a class="page-link" v-if="page != actualPageItems">{{
                    page
                  }}</a>
                  <div class="page-item active" aria-current="page">
                    <span class="page-link" v-if="page === actualPageItems">{{
                      actualPageItems
                    }}</span>
                  </div>
                </li>

                <li class="page-item">
                  <a class="page-link" v-on:click="getNextPageItems()"
                    >Siguiente</a
                  >
                </li>
              </ul>
            </nav>
          </div>
        </div>
      </div>
    </section>
    <div class="float-buttons-container">
      <button class="button create-item-btn" @click="openModal('insumos')">
        INSUMOS
      </button>
    </div>

    <!-- TABLE OUTPUT REPORTS-->
    <div class="main-table-container">
      <table class="custom-responsiva table-items">
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Código</th>
            <th>Item</th>
            <th>Empleado</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="report in paginatedDataOutputReports"
            :key="report"
            id="table_row delete-custom"
          >
            <td>
              {{ dateToString(report.date) }}
              <br />
              {{ convertTimeToLocal(report.time) }}
            </td>
            <td>
              {{ report.item_id }}
            </td>
            <td>
              {{ report.item_name }}
            </td>
            <td>
              {{ report.employee }}
            </td>
          </tr>
        </tbody>
      </table>
      <br />
      <!-- PAGINATION REPORTS -->
      <div class="pagination-container">
        <nav aria-label="Page navigation example">
          <ul class="pagination">
            <li class="page-item">
              <a class="page-link" v-on:click="getPreviousPageOutputReports()"
                >Anterior</a
              >
            </li>
            <li
              v-for="page in paginationOutputReports.totalPages(
                outputReports.length
              )"
              :key="page"
              v-on:click="getDataPageOutputReports(page, outputReports)"
              class="page-item"
            >
              <a class="page-link" v-if="page != actualPageOutputReports">{{
                page
              }}</a>
              <div class="page-item active" aria-current="page">
                <span
                  class="page-link"
                  v-if="page === actualPageOutputReports"
                  >{{ actualPageOutputReports }}</span
                >
              </div>
            </li>

            <li class="page-item">
              <a class="page-link" v-on:click="getNextPageOutputReports()"
                >Siguiente</a
              >
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import { itemServices } from "../service/item-service";
import { paginationItems } from "../paginationItems";
import { paginationOutputReports } from "../paginationOutputReports";
import { employeeServices } from "../service/employee-service";
import { reportServices } from "../service/report-service";
export default {
  name: "Home",
  data: function () {
    return {
      items: [],
      outputReports: [],

      paginationItems: paginationItems,
      paginationOutputReports: paginationOutputReports,
      paginatedDataItems: [],
      paginatedDataOutputReports: [],
      actualPageItems: 1,
      actualPageOutputReports: 1,
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

      item: {
        id: "",
        name: "",
        evidence: "",
      },

      itemUpdate: {
        id: "",
        name: "",
        evidence: "",
      },

      employees: [],
      filterSearch: "",
      newItem: false,
      updateItem: false,
      employeesSelected: [],
      firstPage: true,
      secondPage: false,
      itemsSelected: [],
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
    // ITEM FUNCTIONS

    processCreateItem: function () {
      this.startLoader = true;
      itemServices.createItem(this.item).then((result) => {
        itemServices.getItemsList().then((result) => {
          this.items = result;
          this.startLoader = false;
          this.paginatedDataItems = paginationItems.getDataPage(
            this.actualPageItems,
            this.items
          );
          this.item = {
            id: "",
            name: "",
            evidence: "",
          };
        });
      });
    },

    processUpdateItem: function () {
      itemServices.updateItem(this.itemUpdate).then((result) => {
        this.itemUpdate = {
          id: "",
          name: "",
          evidence: "",
        };
        (this.updateItem = false),
          itemServices.getItemsList().then((result) => {
            this.items = result;
            this.startLoader = false;
            this.paginatedDataItems = paginationItems.getDataPage(
              this.actualPageItems,
              this.items
            );
            this.item = {
              id: "",
              name: "",
              evidence: "",
            };
          });
      });
    },
    processDeleteItem: function (itemId) {
      this.startLoader = true;
      swal({
        title: "¿Estás seguro?",
        text: "Una vez eliminado, no podrás recuperar este elemento",
        icon: "warning",
        buttons: true,
        dangerMode: true,
      }).then((willDelete) => {
        if (willDelete) {
          itemServices.deleteItem(itemId).then((response) => {
            itemServices.getItemsList().then((result) => {
              this.items = result;
              this.startLoader = false;
              this.paginatedDataItems = paginationItems.getDataPage(
                this.actualPageItems,
                this.items
              );
            });
          });
        } else {
          this.startLoader = false;
        }
      });
    },

    closeModal: function (modal) {
      this.modals[modal] = false;
      let home = document.querySelector(".home");
      home.classList.remove("parentDiv");
    },

    // PAGINATION FUNCTIONS FOR ITEMS
    getDataPageItems: function (page, items) {
      this.filterSearch = ""; // borra el filtro
      this.actualPageItems = page;
      this.paginatedDataItems = paginationItems.getDataPage(page, items);
    },

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
    // PAGINATION FUNCTIONS FOR OUTPUT REPORTS
    getDataPageOutputReports: function (page, outputReports) {
      this.filterSearch = ""; // borra el filtro
      this.actualPageOutputReports = page;
      this.paginatedDataOutputReports = paginationOutputReports.getDataPage(
        page,
        outputReports
      );
    },

    getPreviousPageOutputReports: function () {
      this.filterSearch = ""; // borra el filtro
      this.actualPageOutputReports = paginationOutputReports.getPreviousPage(
        this.actualPageOutputReports
      );

      this.paginatedDataOutputReports = paginationOutputReports.getDataPage(
        this.actualPageOutputReports,
        this.outputReports
      );
    },

    getNextPageOutputReports: function () {
      this.filterSearch = ""; // borra el filtro
      this.actualPageOutputReports = paginationOutputReports.getNextPage(
        this.actualPageOutputReports,
        paginationOutputReports.totalPages(this.outputReports.length)
      );

      this.paginatedDataOutputReports = paginationOutputReports.getDataPage(
        this.actualPageOutputReports,
        this.outputReports
      );
    },

    // OTRAS FUNCIONES
    // convert date AAAA-MM-DD to DD/MM/AAAA
    dateToString: function (date) {
      date = date.toString();
      if (date != null && date != undefined) {
        let dateArray = date.split("-");
        dateArray[1] =
          dateArray[1].length == 1 ? "0" + dateArray[1] : dateArray[1];
        dateArray[2] =
          dateArray[2].length == 1 ? "0" + dateArray[2] : dateArray[2];
        return dateArray.join("/");
      }
    },

    // convert time 00:00 to am/pm
    convertTimeToLocal: function (time) {
      if (time != null || time != undefined) {
        let time_array = time.split(":");
        let hour = time_array[0];
        let minute = time_array[1];
        let ampm = "am";
        if (hour >= 12) {
          ampm = "pm";
          if (hour > 12) {
            hour = hour - 12;
          }
        }

        let new_time = hour + ":" + minute + " " + ampm;
        return new_time;
      }
    },

    // DATOS INICIALES DE LA APP
    getInitialData: function () {
      itemServices.getItemsList().then((result) => {
        this.items = result;
        this.totalInitialDataResults += 1;
        this.paginatedDataItems = paginationItems.getDataPage(
          this.actualPageItems,
          this.items
        );
        console.log(this.items[0].id);
      });
      employeeServices.getEmployeesList().then((result) => {
        this.employees = result;
      });
      reportServices.getReportsOutputList().then((result) => {
        this.outputReports = result;
        this.paginatedDataOutputReports = paginationOutputReports.getDataPage(
          this.actualPageOutputReports,
          this.outputReports
        );
      });
    },

    employeeSelected: function () {
      if (!this.employeesSelected.includes(this.employee.name)) {
        this.employeesSelected.push(this.employee.name);
        console.log(this.employeesSelected);
        this.employee.name = "";
      } else {
        alert("Trabajador ya ha sido agregado!");
        this.employee.name = "";
      }
    },

    //pendiente
    searchItem: function (code) {
      for (i in items) {
        if (items[i].id.includes(code)) {
          itemsSelected.push(code);
        }
      }
    },
  },
  created: function () {
    this.verifyAuth();
    this.getInitialData();
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.main {
  width: 100%;
  height: 70%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
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
  cursor: pointer;
}
a {
  color: #42b983;
}

@import "../assets/css/common/modals.css";
@import "../assets/css/common/popUp.css";
@import "../assets/css/common/grid-menu.css";
@import "../assets/css/common/inputs.css";
@import "../assets/css/common/icons.css";
@import "../assets/css/common/button.css";
@import "../assets/css/common/float-buttons.css";
@import "../assets/css/common/links.css";
@import "../assets/css/common/suggestion.css";
@import "../assets/css/base/base.css";
@import "../assets/css/common/table.css";
@import "../assets/css/common/tableMain.css";
@import "../assets/css/common/tableResults.css";
@import "../assets/css/common/lds-ripple.css";
</style>
