<template>
  <div id="app" class="app">
    <!-- id = cual es la aplicación -->

    <div class="header" id="header" v-if="is_auth">
      <nav>
        <p>INVENTORY</p>
        <div class="header-buttons-container">
          <button v-if="is_auth && !startLoader" v-on:click="loadHome">
            Inicio
          </button>
          <button v-if="is_auth && !startLoader" v-on:click="loadHistorial">
            Historial
          </button>
          <button v-if="is_auth && !startLoader" v-on:click="logOut">
            Cerrar Sesión
          </button>
          <button v-if="is_auth && is_admin" v-on:click="loadSignUp">
            Nuevo Usuario
          </button>
          <button v-if="false" v-on:click="loadHistorialGeneralAdmin">
            Admin
          </button>
        </div>
      </nav>
    </div>

    <div class="main-component">
      <!-- funciones a travez de las cuales los hijos van a comunicarse con el padre -->
      <!-- se implementan en export default -->
      <router-view
        v-on:completedLogIn="completedLogIn"
        v-on:completedSignUp="completedSignUp"
        v-on:logOut="logOut"
        v-on:loadHome="loadHome"
        v-on:loadAdmin="loadAdmin"
        v-on:loadSignUp="loadSignUp"
        v-on:loadLogIn="loadLogIn"
        v-on:verifyToken="verifyToken"
      >
      </router-view>
    </div>

    <!--     <div class="footer">
      <h2>Misión TIC 2022</h2>
    </div> -->
  </div>
  <!-- LOADER -->
  <div class="lds-spinner" v-if="startLoader">
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
  </div>
</template>

<script>
import swal from "sweetalert";
import axios from "axios";
import jwt_decode from "jwt-decode";
export default {
  name: "App", // nombre del componente
  data: function () {
    // informacion que va a tener el componente y que se va apoder mostrar dentro el template
    return {
      is_auth: false,
      is_admin: false,
      is_client: false,
      name: "",
      userId: "",
      startLoader: false,
    };
  },

  components: {}, //componentes con los que se va a comunicar
  methods: {
    // metodos que definen el comportamiento que tendrá la aplicación
    verifyAuth: function () {
      this.is_auth = localStorage.getItem("isAuth") || false;
      if (this.is_auth == false) {
        this.$router.push({ name: "logIn" });
      } else {
        this.$router.push({ name: "home" });
        this.getUserData();
      }
    },

    loadHome: function () {
      this.$router.push({ name: "home" });
    },
    loadLogIn: function () {
      this.$router.push({ name: "logIn" });
    },
    loadHistorial: function () {
      this.$router.push({ name: "historial" });
    },
    loadSignUp: function () {
      this.$router.push({ name: "signUp" });
    },
    loadHistorialGeneralAdmin: function () {
      this.$router.push({ name: "historialGeneralAdmin" });
    },
    loadInput: function () {
      this.$router.push({ name: "input" });
    },

    completedLogIn: function (data) {
      localStorage.setItem("isAuth", true);
      localStorage.setItem("email", data.email);
      localStorage.setItem("token_access", data.token_access);
      localStorage.setItem("token_refresh", data.token_refresh);
      /* alert("Autenticación Exitosa"); */
      this.verifyAuth();
    },
    completedSignUp: function (data) {
      swal("Usuario Creado", "", "success");
      this.completedLogIn(data);
    },

    logOut: function () {
      localStorage.clear();
      this.verifyAuth();
    },

    getUserData: async function () {
      this.startLoader = true;
      if (
        localStorage.getItem("token_access") === null ||
        localStorage.getItem("token_refresh") === null
      ) {
        return;
      }
      await this.verifyToken(); // esto se utiliza para esperar a que la sección de comprobación y actualización delaccess token terminen, y que solo cuando hayan terminado

      let token = localStorage.getItem("token_access");
      let userId = jwt_decode(token).user_id.toString();

      axios
        .get(`https://quotation-system-be.herokuapp.com/user/${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          this.is_admin = response.data.is_admin;
          localStorage.setItem("isAdmin", response.data.is_admin);
          this.name = response.data.name;
          localStorage.setItem("name", response.data.name);
          this.loadHome();
          this.startLoader = false;
        })
        .catch((error) => {});
    },

    verifyToken: function () {
      this.startLoader = true;
      return axios
        .post(
          "https://quotation-system-be.herokuapp.com/refresh",
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
  },
  created: function () {
    // funciones que se ejecutan cada vez que se ejecuta el componente
    this.verifyAuth();
  },
};
</script>

<style>
@import "./assets/css/colors.css";
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  font-weight: 300;
}
body {
  font-family: "Source Sans Pro", sans-serif;
  background-color: var(--color-secondary);
  color: white;
  font-weight: 300;
  margin: 0 0 0 0;
  min-height: 100%;
  height: 100%;
  position: relative;
}

p {
  margin-bottom: 0 !important;
}

body ::-webkit-input-placeholder {
  /* WebKit browsers */
  font-family: "Source Sans Pro", sans-serif;
  color: white;
  font-weight: 300;
}
body :-moz-placeholder {
  /* Mozilla Firefox 4 to 18 */
  font-family: "Source Sans Pro", sans-serif;
  color: white;
  opacity: 1;
  font-weight: 300;
}
body ::-moz-placeholder {
  /* Mozilla Firefox 19+ */
  font-family: "Source Sans Pro", sans-serif;
  color: white;
  opacity: 1;
  font-weight: 300;
}
body :-ms-input-placeholder {
  /* Internet Explorer 10+ */
  font-family: "Source Sans Pro", sans-serif;
  color: white;
  font-weight: 300;
}

.header-buttons-container {
  float: right;
  width: 50%;
  display: flex;
  justify-content: right;
  align-content: center;
}

#header {
  margin: 0%;
  padding: 0;
  width: 100%;
  height: 7vh;
  min-height: 30px;
  color: #030f1b;
  justify-content: center;
  align-items: center;
  align-items: center;
  position: inherit !important;
  background-color: var(--color-secondary-dark);
  z-index: 2;
}
.header nav {
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: right;
  padding-right: 5%;
  align-items: center;
}
.header nav button {
  color: #e5e7e9;
  background: var(--secondary-color);
  border-radius: 5px;
  padding: 2px 8px;
  margin: 0 5px;
  cursor: pointer;
  font-weight: 500;
  border: none;
  font-size: 17px;
}
.header nav button:hover {
  color: #283747;
  background: #e5e7e9;
}

.header nav p {
  width: 50%;
  float: left;
  color: #ffffff;
  font-weight: 600;
  margin-left: 5rem;
}

.app {
  height: 100vh;
}

.main-component {
  margin: 0%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
.footer {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 10vh;
  min-height: 100px;
  background-color: #262626;
  color: #e5e7e9;
}
.footer h2 {
  width: 100%;
  height: 100%;

  display: flex;
  justify-content: center;
  align-items: center;
}

@media (max-width: 768px) {
  .header nav {
    width: 100%;
  }
  .header nav button {
    margin: 0 5px !important;
    padding: 5px 6px 5px 6px !important;
    font-size: 14px;
  }
  .header nav p {
    margin-right: 15%;
    color: #ffffff;
  }
}

/* class input if intem exist */
.itemExist {
  border: 1.5px solid red !important;
}

/* class input if item is Empty */
.inputEmpty {
  border: 1.5px solid red !important;
}

.atras_container {
  padding: 10px;
  text-align: center;
}

@import "./assets/css/common/reqStatus.css";
@import "./assets/css/common/loader.css";
</style>