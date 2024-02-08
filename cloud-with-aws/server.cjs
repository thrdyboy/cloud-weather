const express = require('express');
const app = express();

app.use(express.static('public')); // Direktori berkas statis (situs web Anda)

const PORT = 8000;
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
