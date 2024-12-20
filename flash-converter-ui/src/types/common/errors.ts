/**
 * Validation error response from the API.
 */
export interface ValidationError {

  /**
   * The location of the error in the input data.
   */
  loc: (string | number)[];

  /**
   * A human-readable message describing the error.
   */
  msg: string;

  /**
   * A string indicating the error type.
   */
  type: string;
}

/**
 * Validation error response from the API.
 */
export interface HTTPValidationError {
  /**
   * A list of validation errors.
   */
  detail: ValidationError[];
}