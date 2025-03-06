<template>
  <div class="login-container">
    <!-- Debug info -->
    <div class="debug-info">
      <p>Updated login to work with proper backend proxy configuration</p>
    </div>
    
    <!-- HTML fallback form -->
    <div class="fallback-form" style="margin: 20px; padding: 20px; background: white; border: 2px solid #333; border-radius: 8px;">
      <h2 style="text-align: center; color: black; margin-bottom: 20px;">Login Form</h2>
      
      <div style="margin-bottom: 15px;">
        <label style="display: block; margin-bottom: 5px; color: black; font-weight: bold;">Username:</label>
        <input 
          type="text" 
          v-model="username" 
          style="width: 100%; padding: 10px; border: 1px solid #666; border-radius: 4px;"
        >
      </div>
      
      <div style="margin-bottom: 15px;">
        <label style="display: block; margin-bottom: 5px; color: black; font-weight: bold;">Password:</label>
        <div style="display: flex;">
          <input 
            type="password" 
            v-model="password"
            style="width: 100%; padding: 10px; border: 1px solid #666; border-radius: 4px;"
          >
          <button 
            @click="generatePassword"
            style="margin-left: 10px; padding: 10px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; white-space: nowrap;"
            title="Generate a strong password"
          >
            Generate
          </button>
        </div>
        <div v-if="generatedPassword" style="margin-top: 10px; padding: 10px; background: #f8f8f8; border: 1px dashed #999; border-radius: 4px;">
          <p style="margin: 0; font-family: monospace; color: black;">Generated password: <strong>{{ generatedPassword }}</strong></p>
          <small style="color: #666;">This password is compatible with the system's encryption. Copy it to a secure location.</small>
          <button 
            @click="useGeneratedPassword"
            style="margin-top: 10px; padding: 5px 10px; background: #607D8B; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px;"
          >
            Use this password
          </button>
        </div>
      </div>
      
      <div v-if="loginError" style="margin-top: 10px; padding: 10px; background: #ffebee; color: #d32f2f; border: 1px solid #ffcdd2; border-radius: 4px;">
        {{ loginError }}
      </div>
      
      <button 
        @click="loginUser"
        style="width: 100%; padding: 12px; background: #1867C0; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; margin-top: 20px;"
      >
        Login
      </button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router'

export default {
  data() {
    return {
      username: '',
      password: '',
      generatedPassword: '',
      loginError: '',
      isLoading: false
    }
  },
  methods: {
    setAuthToken(token) {
      localStorage.setItem('auth', token)
    },
    
    setAccessLevels(token) {
      localStorage.setItem('access_levels', token)
    },
    
    goToDashboard() {
      // Always redirect to statements after login
      this.$router.push({ name: 'statements' });
    },
    
    generatePassword() {
      // Generate a strong password that works with Werkzeug's password hashing
      const length = 12;
      const uppercaseChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
      const lowercaseChars = 'abcdefghijklmnopqrstuvwxyz';
      const numberChars = '0123456789';
      const specialChars = '!@#$%^&*()_+[]{}|;:,.<>?';
      
      const allChars = uppercaseChars + lowercaseChars + numberChars + specialChars;
      let password = '';
      
      // Ensure at least one char of each type
      password += uppercaseChars.charAt(Math.floor(Math.random() * uppercaseChars.length));
      password += lowercaseChars.charAt(Math.floor(Math.random() * lowercaseChars.length));
      password += numberChars.charAt(Math.floor(Math.random() * numberChars.length));
      password += specialChars.charAt(Math.floor(Math.random() * specialChars.length));
      
      // Fill the rest randomly
      for (let i = 4; i < length; i++) {
        password += allChars.charAt(Math.floor(Math.random() * allChars.length));
      }
      
      // Shuffle the password
      password = password.split('').sort(() => 0.5 - Math.random()).join('');
      
      this.generatedPassword = password;
    },
    
    useGeneratedPassword() {
      this.password = this.generatedPassword;
      this.generatedPassword = '';
    },
    
    async loginUser() {
      this.loginError = '';
      this.isLoading = true
      
      try {
        console.log("Login attempt with:", this.username, this.password);
        
        // Use the exact endpoint that matches the backend route
        const url = '/employee/auth/login';
        
        // First try with FormData (which is what one of the backend routes expects)
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
            
            this.setAuthToken(data.jwt_token);
            if (data.access_levels) {
              this.setAccessLevels(JSON.stringify(data.access_levels));
            }
            
            console.log("Redirecting to statements...");
            this.goToDashboard();
            return;
          } else if (formResponse.status === 404) {
            // This is the expected error for invalid credentials
            const errorData = await formResponse.json();
            throw new Error(errorData.detail || 'Invalid username or password');
          } 
        } catch (formError) {
          console.error('FormData login attempt failed:', formError);
        }
        
        // Then try with JSON format (for the second route handler)
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
            
            this.setAuthToken(data.jwt_token);
            if (data.access_levels) {
              this.setAccessLevels(JSON.stringify(data.access_levels));
            }
            
            console.log("Redirecting to statements...");
            this.goToDashboard();
            return;
          }
        } catch (jsonError) {
          console.error('JSON login attempt failed:', jsonError);
        }
        
        // If all attempts fail, throw a more descriptive error
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
    // Check if already logged in
    if (localStorage.getItem('auth')) {
      console.log("User already logged in, redirecting...");
      this.goToDashboard();
    }
  }
}
</script>

<style>
.login-container {
  width: 100%;
  max-width: 500px;
  margin: 40px auto;
}

.debug-info {
  background: #ffeb3b;
  color: #000;
  text-align: center;
  padding: 10px;
  margin-bottom: 20px;
  font-weight: bold;
  border: 2px solid #f57f17;
}
</style>
