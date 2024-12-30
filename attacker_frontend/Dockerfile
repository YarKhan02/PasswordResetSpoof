# Use an official Nginx image as the base image
FROM nginx:alpine

# Set the working directory inside the container
WORKDIR /usr/share/nginx/html

# Remove the default Nginx static files
RUN rm -rf ./*

# Copy all files from the src directory to the Nginx HTML directory
COPY src/ /usr/share/nginx/html

# Expose port 80 to serve the content
EXPOSE 80

# Start the Nginx server
CMD ["nginx", "-g", "daemon off;"]
