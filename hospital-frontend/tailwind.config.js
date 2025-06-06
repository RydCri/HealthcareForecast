export default {
    server: {
        proxy: {
            '/api': 'http://localhost:5000'
        }
    },
    content: ["./index.html", "./**/*.js"]

}
