<template>
  <main class="register">
    <!-- SECTION LOGIN HEADER -->
    <section class="register__header">
      <br />
      <img src="../assets/img/logo_img.png" alt="" class="register__img" />
      <h2 class="register__title">Lavadero App</h2>
      <h1 class="register__subtitle">Registrar nuevo usuario</h1>
    </section>

    <!-- SECTION REGISTER FORM -->
    <form v-on:submit.prevent="processSignUp" class="register__form">
      <div class="register__item">
        <span class="register__text">Correo Electrónico</span>
        <i class="fas fa-envelope"></i>
        <input
          class="register__input"
          type="email"
          v-model="user.email"
          id="email"
          name="email"
          placeholder="correo"
          required
        />
      </div>
      <div class="register__item">
        <span class="register__text">Contraseña</span>
        <i class="fas fa-lock"></i>
        <input
          class="register__input"
          type="password"
          v-model="user.password"
          name="password"
          id="password"
          placeholder="contraseña"
          required
        />
      </div>
      <div class="register__errors">
        <i
          class="fa fa-exclamation-circle"
          id="error-icon"
          v-if="error_message"
        ></i>
        <span v-if="error_message" class="register__text text_fail">{{
          " " + error_message
        }}</span>
      </div>
      <div class="register__item">
        <span class="register__text">Nombre</span>
        <i class="fas fa-envelope"></i>
        <input
          class="register__input"
          type="text"
          v-model="user.name"
          id="name"
          name="name"
          placeholder="nombre"
          required
        />
      </div>
      <div class="register__item">
        <span class="register__text">¿Usuario Administrador?</span>
        <br />
        <section title=".admin">
          <!-- .slideThree -->
          <div class="slideThree">
            <input
              type="checkbox"
              v-model="user.is_admin"
              value="true"
              id="slideThree"
              name="check"
              checked
            />
            <label for="slideThree"></label>
          </div>
          <!-- end .slideThree -->
        </section>
      </div>
      <div class="register__item">
        <span class="register__text">¿Usuario Cliente?</span>
        <br />
      </div>
      <button type="submit" class="register__submit">Registrar</button>
      <br />
      <br />
    </form>

    <!-- ANIMATED BACKGROUND -->
    <ul class="bg-bubbles">
      <li></li>
      <li></li>
      <li></li>
      <li></li>
      <li></li>
      <li></li>
      <li></li>
      <li></li>
      <li></li>
      <li></li>
    </ul>
  </main>

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
import axios from "axios";
import jwt_decode from "jwt-decode";
export default {
  name: "SignUp",
  data: function () {
    return {
      user: {
        email: "",
        password: "",
        name: "",
        is_admin: false,
      },
      cajaMenor: {
        user: "",
      },
      error_message: "",
      error_signup: false,
      is_admin: false,
      startLoader: false,
    };
  },
  methods: {
    verifyAuth: function () {
      this.is_auth = localStorage.getItem("isAuth") || false;
      if (this.is_auth == false) {
        this.$router.push("logIn");
      }
    },
    processSignUp: function () {
      this.startLoader = true;
      axios
        .post("https://quotation-system-be.herokuapp.com/register", this.user, {
          headers: {},
        })
        .then((result) => {
          let dataSignUp = {
            email: this.user.email,
            token_access: result.data.access,
            token_refresh: result.data.refresh,
          };
          let token = result.data.access;
          let userId = jwt_decode(token).user_id;
          this.processCreateCajaMenor(userId);
          this.startLoader = false;
          this.$emit("completedSignUp", dataSignUp);
        })
        .catch((error) => {
          console.log(error);
          if (error.response.status == "401") {
            this.error_message = "El correo ya está registrado";
            this.error_signup = true;
          } else if (error.response.status == "400") {
            this.error_message = "El correo ya está registrado";
            this.error_signup = true;
          } else if (error.response.status == "500") {
            this.error_message = "Error en el servidor";
            this.error_signup = true;
          } else {
            this.error_message = "Error en el servidor";
            this.error_signup = true;
          }
          this.startLoader = false;
        });
    },

    processCreateCajaMenor: async function (userIdCreated) {
      this.cajaMenor.user = userIdCreated;
      this.startLoader = true;
      if (
        localStorage.getItem("token_access") === null ||
        localStorage.getItem("token_refresh") === null
      ) {
        this.$emit("logOut");
        return;
      }
      await this.verifyToken(); // esto se utiliza para esperar a que la sección de comprobación y actualización delaccess token terminen, y que solo cuando hayan terminado

      let token = localStorage.getItem("token_access");
      let userId = jwt_decode(token).user_id.toString();
      axios
        .post(
          `https://quotation-system-be.herokuapp.com/cajaMenor/${userId}`,
          this.cajaMenor,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )
        .then((response) => {
          this.startLoader = false;
        })
        .catch((error) => {
          console.log(error);
          if (error.response.status == "401") {
            this.error_message = "Error en el servidor";
            this.error_createequipo = true;
          } else if (error.response.status == "400") {
            this.error_message = "Error en el servidor";
            this.error_createequipo = true;
          } else if (error.response.status == "500") {
            this.error_message = "Error en el servidor";
            this.error_createequipo = true;
          } else {
            this.error_message = "Error en el servidor";
            this.error_createequipo = true;
          }
          this.startLoader = false;
        });
    },
    verifyToken: function () {
      return axios
        .post(
          "https://quotation-system-be.herokuapp.com/refresh",
          { refresh: localStorage.getItem("token_refresh") },
          { headers: {} }
        )
        .then((result) => {
          localStorage.setItem("token_access", result.data.access);
        })
        .catch(() => {
          this.$emit("logOut");
        });
    },
  },
  created: function () {
    this.verifyAuth();
  },
};
</script>     


<style>
@import "../assets/css/signUp/signUp.css";
@import "../assets/css/signUp/signUp-header.css";
@import "../assets/css/signUp/signUp-form.css";
/* estilos del checkbox */
@import "../assets/css/signUp/slideThree.css";
/* bg-bubbles */
@import "../assets/css/common/bg-bubbles.css";
</style>