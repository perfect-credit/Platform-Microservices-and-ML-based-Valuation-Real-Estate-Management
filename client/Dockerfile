# Step 1: Use Node v22 for building the app
FROM node:22.11.0-alpine AS builder

# Set the working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json* ./
RUN npm install --frozen-lockfile

# Copy the rest of the application code
COPY . .

# Expose the port SvelteKit runs on (default for Vite is 5173)
EXPOSE 5173

# Run the app in development mode
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
