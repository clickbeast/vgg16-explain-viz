# AUTO GENERATED FILE - DO NOT EDIT

#' @export
matrix <- function(id=NULL, hoverColor=NULL, selectedColor=NULL, selectedLayer=NULL) {
    
    props <- list(id=id, hoverColor=hoverColor, selectedColor=selectedColor, selectedLayer=selectedLayer)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'Matrix',
        namespace = 'ssp_matrix',
        propNames = c('id', 'hoverColor', 'selectedColor', 'selectedLayer'),
        package = 'sspMatrix'
        )

    structure(component, class = c('dash_component', 'list'))
}
