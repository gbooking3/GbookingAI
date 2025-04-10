import { Link } from "react-router-dom";
import Button from 'react-bootstrap/Button';
/**
 * @component PageNotFound
 * @description
 * Displays a custom 404 error page when the user navigates to a non-existent route.
 * The component includes an image and a button to navigate back to the home page.
 *
 * @dependencies
 *  - React Hooks: useState.
 *  - React Router: Link.
 *  - External Library: react-bootstrap (Button).
 *  - i18next: useTranslation for translation functionality.
 *
 * @returns {JSX.Element}
 *  - article: HTML article element containing the error image and navigation button.
 *    - div (d-flex justify-content-center): Flex container for centering the image.
 *      - img: Image element displaying the custom error image.
 *    - div (d-flex justify-content-center): Flex container for centering the navigation button.
 *      - Link: React Router Link component wrapping the navigation button.
 *        - Button: Bootstrap Button component linking back to the home page.
 */
const NotFoundPage = () => {

  return (
    <article>
      {/* Display the error image centered */}
      <div className="d-flex justify-content-center">
        <img src="src/assets/images/404.svg" alt="svg" height="500" />
      </div>
      
      {/* Display the navigation button centered */}
      <div className="d-flex justify-content-center">
        <Link to="/">
          {/* Button to navigate back to the home page */}
          <Button variant="outline-secondary">Back_to_Home</Button>
        </Link>
      </div>
    </article>
  );
};

export default NotFoundPage;
