<template>
  <div class="main">
    <!-- SECTION SEARCH FILTER -->
    <section class="search-and-user">
      <form>
        <input
          type="search"
          placeholder="Buscar..."
          id="input_search_clientes"
          v-model="defaultInputSearch"
          v-on:input="filterBySearch"
        />
        <button type="submit" aria-label="submit form">
          <li class="fas fa-search"></li>
        </button>
      </form>
    </section>

    <section class="table-container-two">
      <!-- TABLE OUTPUT REPORTS-->
      <div class="main-table-container">
        <table class="custom-responsiva table-items">
          <thead>
            <tr>
              <th>Fecha</th>
              <th>Código</th>
              <th>Item</th>
              <th>Empleado</th>
              <th>Estado</th>
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
              <td>
                {{ report.status }}
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
                v-for="page in paginationReports.totalPages(
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
    </section>
  </div>
</template>
<script>
import axios from "axios";
import { itemServices } from "../service/item-service";
import { paginationItems } from "../paginationItems";
import { paginationReports } from "../paginationReports";
import { employeeServices } from "../service/employee-service";
import { reportServices } from "../service/report-service";
import swal from "sweetalert2";
export default {
  name: "Historial",
  data: function () {
    return {
      items: [],
      outputReports: [],

      paginationReports: paginationReports,
      paginatedDataOutputReports: [],
      actualPageItems: 1,
      actualPageOutputReports: 1,
      startLoader: false,

      itemReport: {
        item: "",
        status: "",
        observation: "",
        employee: "",
      },

      employees: [],
      filterSearch: "",
      newItem: false,
      newComment: false,
      updateItem: false,
      employeesSelected: [],
      firstPage: true,
      secondPage: false,
      itemsSelected: [],
      initialDataCounter: 0,
      initialDataElements: ["items", "employees", "reports"],
      circle1: null,
      text1: "",
      showProgressBar: false,
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
      // iterar objeto
      for (let key in this.modals) {
        if (key != modal) {
          this.modals[key] = false;
        }
      }
      this.modals[modal] = true;
      if (modal != "home") {
        let home = document.querySelector(".home");
        home.classList.add("parentDiv");
        home.classList.remove("absolute");
      }

      if (modal === "input") {
        setTimeout(function () {
          let input = document.getElementById("input-entrada");
          input.focus();
        }, 100);
      }
    },

    getEmployees: function () {
      employeeServices.getEmployeesList().then((result) => {
        this.employees = result;
      });
    },

    getOutputReports: function () {
      this.outputReports = [];
      reportServices.getReportsOutputList().then((result) => {
        this.outputReports = result;

        this.paginatedDataOutputReports = paginationReports.getDataPage(
          1,
          this.outputReports
        );
        this.comproveProgressBarLoad();
      });
    },
    // ITEM FUNCTIONS

    processCreateItem: function () {
      this.startLoader = true;
      itemServices.createItem(this.item).then((result) => {
        itemServices.getItemsList().then((result) => {
          this.items = result;
          this.startLoader = false;
          this.paginatedDataItems = paginationItems.getDataPage(1, this.items);
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
      this.paginatedDataOutputReports = paginationReports.getDataPage(
        page,
        outputReports
      );
    },

    getPreviousPageOutputReports: function () {
      this.filterSearch = ""; // borra el filtro
      this.actualPageOutputReports = paginationReports.getPreviousPage(
        this.actualPageOutputReports
      );

      this.paginatedDataOutputReports = paginationReports.getDataPage(
        this.actualPageOutputReports,
        this.outputReports
      );
    },

    getNextPageOutputReports: function () {
      this.filterSearch = ""; // borra el filtro
      this.actualPageOutputReports = paginationReports.getNextPage(
        this.actualPageOutputReports,
        paginationReports.totalPages(this.outputReports.length)
      );

      this.paginatedDataOutputReports = paginationReports.getDataPage(
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

    deleteItemSelected: function (item) {
      this.itemsSelected = this.itemsSelected.filter((i) => i != item);
      let input = document.getElementById("items-selected-input");
      input.focus();
    },

    deleteEmployeeSelected: function (employee) {
      this.employeesSelected = this.employeesSelected.filter(
        (i) => i != employee
      );
    },

    // Comprobar si los datos iniciales ya fueron completados para desactivar el loader
    comproveInitialData: function () {
      this.initialDataCounter += 1;
      if (this.initialDataCounter === this.initialDataElements.length) {
        this.startLoader = false;
      }
    },

    // DATOS INICIALES DE LA APP
    getInitialData: function () {
      this.startLoader = true;

      reportServices.getReportsList().then((result) => {
        this.outputReports = result;
        this.paginatedDataOutputReports = paginationReports.getDataPage(
          this.actualPageOutputReports,
          this.outputReports
        );
        this.comproveProgressBarLoad();
        this.comproveInitialData();
      });
    },

    employeeSelected: function () {
      if (!this.employeesSelected.includes(this.employee.name)) {
        this.employeesSelected.push(this.employee.name);
        this.employee.name = "";
      } else {
        alert("Trabajador ya ha sido agregado!");
        this.employee.name = "";
      }
    },

    //pendiente
    searchItem: function (code) {
      const Swal = require("sweetalert2");
      let itemsId = this.items.map((item) => item.id);
      if (itemsId.includes(code.trim())) {
        let item = this.items.filter((item) => item.id === code);
        if (!this.itemsSelected.includes(item[0])) {
          item[0].showTextArea = false;
          this.itemsSelected.push(item[0]);
        } else if (this.itemsSelected.includes(item[0])) {
          Swal.fire({
            position: "top",
            icon: "warning",
            title: "No se puede registrar dos veces!",
            showConfirmButton: false,
            timer: 1500,
          });
        }
        this.item.id = "";
        let input = document.getElementById("items-selected-input");
        input.focus();
      }
    },

    //funcion para crear un reporte desde secondPage
    processCreateReport: function (reportType) {
      const Swal = require("sweetalert2");
      this.startLoader = true;
      if (
        this.itemsSelected.length != 0 &&
        this.employeesSelected.length != 0 &&
        reportType === "output"
      ) {
        this.itemsSelected.forEach((item) => {
          let outputReport = {
            item: item.id,
            status: "output",
            observation: item.observation,
            employee: this.employeesSelected.join(", "),
          };
          reportServices.createReport(outputReport).then((result) => {
            this.getOutputReports();
            Swal.fire({
              position: "top",
              icon: "success",
              title: "Realizado con exito",
              showConfirmButton: false,
              timer: 1500,
            });
          });
        });

        if (reportType != "input") {
          this.openModal("home");
        }
        this.itemsSelected = [];
        this.employeesSelected = [];
        this.secondPage = false;
        this.firstPage = true;
      } else {
        Swal.fire({
          position: "top",
          icon: "warning",
          title: "Completa todos los pasos",
          showConfirmButton: false,
          timer: 1500,
        });
      }
      //Ventana modal
      if (reportType === "input") {
        reportServices.createReport(this.inputReport).then((result) => {
          this.getOutputReports();
          this.inputReport.item = "";
          Swal.fire({
            position: "top",
            icon: "success",
            title: "Realizado con exito",
            showConfirmButton: false,
            timer: 200,
          });
          if (this.showProgressBar === true) {
            this.openModal("home");
          }
        });
      }
    },
    focusInput: function (idInput) {
      setTimeout(function () {
        let input = document.getElementById(idInput);
        input.focus();
      }, 100);
    },

    comproveProgressBarLoad: function () {
      if (this.outputReports.length === 0) {
        this.showProgressBar = true;
        setTimeout(function () {
          this.circle1 = document.getElementById("two");
          this.text1 = document.getElementById("percent-two");
          (function () {
            var angle1 = 0;
            var percent1 = 100 * 4.7;

            let timer1 = window.setInterval(
              function () {
                circle1.setAttribute("stroke-dasharray", angle1 + ", 20000");
                text1.innerHTML =
                  parseInt((angle1 / 475) * 100).toString() + "%";

                if (angle1 >= percent1) {
                  window.clearInterval(timer1);
                }
                angle1 += 7;
              }.bind(this),
              30
            );
          })();
        }, 100);
      } else {
        this.showProgressBar = false;
      }
    },

    progressBarLoad: function (circle1, text1) {
      (function () {
        var angle1 = 0;
        var percent1 = 100 * 4.7;

        let timer1 = window.setInterval(
          function () {
            circle1.setAttribute("stroke-dasharray", angle1 + ", 20000");
            text1.innerHTML = parseInt((angle1 / 475) * 100).toString() + "%";

            if (angle1 >= percent1) {
              window.clearInterval(timer1);
            }
            angle1 += 7;
          }.bind(this),
          30
        );
      })();
    },
    imprimir: function (value) {
      console.log(value);
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
  position: absolute;
  z-index: 10;
}

.inherit {
  position: inherit;
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
@import "../assets/css/common/itemsSelectedList.css";
@import "../assets/css/common/suggestion.css";
@import "../assets/css/base/base.css";
@import "../assets/css/common/table.css";
@import "../assets/css/common/tableMain.css";
@import "../assets/css/common/tableResults.css";
@import "../assets/css/common/lds-ripple.css";
@import "../assets/css/common/percentage.css";
</style>
