readonly LIB_DIR="${BASH_SOURCE%/*}/lib"

if [[ "${SOURCED_SHARED_LIB}" != "true" ]]; then
  source "${LIB_DIR}/log.sh"
  SOURCED_SHARED_LIB="true"
fi
