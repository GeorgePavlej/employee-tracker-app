<template>
  <div class="login-container">
    <div class="login-card">
      <div class="logo-container">
        <div class="logo">
          <v-icon size="40" color="white">mdi-tooth</v-icon>
        </div>
      </div>
      
      <div class="app-title">OrthoDent Pro Access</div>
      
      <div class="login-form">
        <div class="input-group">
          <label>Používateľské meno</label>
          <div class="input-with-icon">
            <v-icon size="small" color="grey" class="input-icon">mdi-email-outline</v-icon>
            <input 
              type="email" 
              v-model="username"
            >
          </div>
        </div>
        
        <div class="input-group">
          <label>Heslo</label>
          <div class="input-with-icon">
            <v-icon size="small" color="grey" class="input-icon">mdi-lock-outline</v-icon>
            <input 
              :type="showPassword ? 'text' : 'password'" 
              v-model="password"
            >
            <v-icon 
              size="small" 
              color="grey" 
              class="password-toggle"
              @click="showPassword = !showPassword"
            >
              {{ showPassword ? 'mdi-eye-off' : 'mdi-eye' }}
            </v-icon>
          </div>
        </div>
        
        <div v-if="loginError" class="error-message">
          {{ loginError }}
        </div>
        
        <button
          @click="loginUser"
          class="login-button"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Logging in...' : 'Login' }}
        </button>
        
        <div class="form-footer">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { saveTokens } from '../utils/auth';

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      showPassword: false,
      loginError: '',
      isLoading: false,
      generatedPassword: ''
    }
  },
  methods: {
    setAuthToken(token) {
      saveTokens(token);
    },
    
    goToDashboard() {
      this.$router.push({ name: 'dashboard' });
    },
    
    async loginUser() {
      this.loginError = '';
      this.isLoading = true
      
      try {
        console.log("Login attempt with:", this.username, this.password);
        
        const baseURL = process.env.VUE_APP_API_URL || '';
        const url = `${baseURL}/employee/auth/login`;
        
        console.log(`Using API URL: ${url}`);
        
        try {
          console.log(`Trying FormData login to ${url}`);
          
          const formData = new FormData();
          formData.append('username', this.username);
          formData.append('password', this.password);
          
          const formResponse = await fetch(url, {
            method: 'POST',
            body: formData
          });
          
          console.log(`FormData response status: ${formResponse.status}`);
          
          if (formResponse.status === 200) {
            const data = await formResponse.json();
            console.log('Login successful with FormData!', data);
            
            saveTokens(data.jwt_token, data.access_levels);
            
            console.log("Redirecting to dashboard...");
            this.goToDashboard();
            return;
          } else if (formResponse.status === 404) {
            const errorData = await formResponse.json();
            throw new Error(errorData.detail || 'Invalid username or password');
          } 
        } catch (formError) {
          console.error('FormData login attempt failed:', formError);
        }
        
        try {
          console.log(`Trying JSON login to ${url}`);
          
          const jsonResponse = await fetch(url, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              username: this.username,
              password: this.password
            })
          });
          
          console.log(`JSON response status: ${jsonResponse.status}`);
          
          if (jsonResponse.status === 200) {
            const data = await jsonResponse.json();
            console.log('Login successful with JSON!', data);
            
            saveTokens(data.jwt_token, data.access_levels);
            
            console.log("Redirecting to dashboard...");
            this.goToDashboard();
            return;
          }
        } catch (jsonError) {
          console.error('JSON login attempt failed:', jsonError);
        }
        
        throw new Error('Login failed. Please check your credentials and try again, or contact support if the issue persists.');
        
      } catch (error) {
        console.error('Login error:', error);
        this.loginError = error.message;
      } finally {
        this.isLoading = false;
      }
    }
  },
  mounted() {
    console.log("Login component mounted using Options API");
    if (localStorage.getItem('auth')) {
      console.log("User already logged in, redirecting...");
      this.goToDashboard();
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 360px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-bottom: 20px;
}

.logo-container {
  display: flex;
  justify-content: center;
  margin-top: 30px;
  margin-bottom: 10px;
}

.logo {
  width: 70px;
  height: 70px;
  background-color: #3f51b5;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.app-title {
  font-size: 14px;
  margin-bottom: 20px;
  color: #333;
}

.login-form {
  width: 85%;
}

.input-group {
  margin-bottom: 20px;
}

.input-group label {
  display: block;
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.input-with-icon {
  position: relative;
  display: flex;
  align-items: center;
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
}

.input-icon {
  position: absolute;
  left: 10px;
}

.input-with-icon input {
  width: 100%;
  padding: 12px 12px 12px 40px;
  border: none;
  outline: none;
  font-size: 14px;
}

.password-toggle {
  position: absolute;
  right: 10px;
  cursor: pointer;
}

.login-button {
  width: 100%;
  padding: 12px;
  background-color: #3f51b5;
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  margin-top: 10px;
  transition: background-color 0.3s;
}

.login-button:hover {
  background-color: #303f9f;
}

.login-button:disabled {
  background-color: #9fa8da;
  cursor: not-allowed;
}

.form-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
  font-size: 14px;
}

.footer-link {
  color: #666;
  text-decoration: none;
}

.footer-link:hover {
  text-decoration: underline;
}

.error-message {
  color: #f44336;
  font-size: 14px;
  margin-top: 10px;
  margin-bottom: 10px;
}
</style> 