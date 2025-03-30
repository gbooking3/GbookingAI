import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Add from "./pages/adduser";


export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Add />}>



        </Route>
      </Routes>
    </BrowserRouter>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);