<template>
  <div class="main">
    <!-- SECTION SEARCH FILTER -->
    <section class="search-and-user">
      <form>
        <input
          type="search"
          placeholder="Buscar..."
          id="input_search_clientes"
          v-model="inputSearch"
          v-on:input="filterBySearch"
          autoComplete="off"
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
              v-for="report in paginatedDataReports"
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
                <a class="page-link" v-on:click="getPreviousPageReports()"
                  >Anterior</a
                >
              </li>
              <li
                v-for="page in paginationReports.totalPages(
                  outputReports.length
                )"
                :key="page"
                v-on:click="getDataPageReports(page, outputReports)"
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
                <a class="page-link" v-on:click="getNextPageReports()"
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
import { paginationItems } from "../paginationItems";
import { paginationReports } from "../paginationReports";
import { reportServices } from "../service/report-service";
export default {
  name: "Historial",
  data: function () {
    return {
      items: [],
      itemReports: [],
      outputReports: [],

      paginationReports: paginationReports,
      paginatedDataReports: [],
      actualPageItems: 1,
      actualPageOutputReports: 1,
      startLoader: false,

      itemReport: {
        item: "",
        status: "",
        observation: "",
        employee: "",
      },

      filterSearch: "",
      firstPage: true,
      secondPage: false,
      itemsSelected: [],
      initialDataCounter: 0,
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

    getOutputReports: function () {
      this.outputReports = [];
      reportServices.getReportsOutputList().then((result) => {
        this.outputReports = result;

        this.paginatedDataReports = paginationReports.getDataPage(
          1,
          this.outputReports
        );
      });
    },
    // ITEM FUNCTIONS

    // PAGINATION FUNCTIONS FOR ITEMS

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
    getDataPageReports: function (page, outputReports) {
      this.filterSearch = ""; // borra el filtro
      this.actualPageOutputReports = page;
      this.paginatedDataReports = paginationReports.getDataPage(
        page,
        outputReports
      );
    },

    getPreviousPageReports: function () {
      this.filterSearch = ""; // borra el filtro
      this.actualPageOutputReports = paginationReports.getPreviousPage(
        this.actualPageOutputReports
      );

      this.paginatedDataReports = paginationReports.getDataPage(
        this.actualPageOutputReports,
        this.outputReports
      );
    },

    getNextPageReports: function () {
      this.filterSearch = ""; // borra el filtro
      this.actualPageOutputReports = paginationReports.getNextPage(
        this.actualPageOutputReports,
        paginationReports.totalPages(this.outputReports.length)
      );

      this.paginatedDataReports = paginationReports.getDataPage(
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
        localStorage.setItem("reports", this.outputReports);
        this.paginatedDataReports = paginationReports.getDataPage(
          this.actualPageOutputReports,
          this.outputReports
        );
      });
    },

    filterBySearch: function () {
      let reports = JSON.parse(localStorage.getItem("reports"));
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
