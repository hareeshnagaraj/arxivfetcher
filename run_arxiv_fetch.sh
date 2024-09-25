#!/bin/bash

# Function to print usage information
print_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  -q, --query QUERY    Run arXiv query with the specified search term"
    echo "  -n, --num NUMBER     Specify the number of results to fetch (default: 5)"
    echo "  -h, --help           Display this help message"
}

# Function to activate virtual environment
activate_venv() {
    source arxiv_env/bin/activate
}

# Function to deactivate virtual environment
deactivate_venv() {
    deactivate
}

# Function to run arXiv query
run_arxiv_query() {
    python arxiv_query.py "$1" "$2"
}

# Main script logic
main() {
    if [ $# -eq 0 ]; then
        print_usage
        exit 1
    fi

    local query=""
    local num_results=5

    while [ $# -gt 0 ]; do
        case "$1" in
            -q|--query)
                if [ -n "$2" ]; then
                    query="$2"
                    shift 2
                else
                    echo "Error: -q|--query requires a search term"
                    exit 1
                fi
                ;;
            -n|--num)
                if [ -n "$2" ] && [[ "$2" =~ ^[0-9]+$ ]]; then
                    num_results=$2
                    shift 2
                else
                    echo "Error: -n|--num requires a positive integer"
                    exit 1
                fi
                ;;
            -h|--help)
                print_usage
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                print_usage
                exit 1
                ;;
        esac
    done

    if [ -z "$query" ]; then
        echo "Error: No query specified. Use -q or --query to specify a search term."
        exit 1
    fi

    activate_venv

    echo "Running arXiv query for: $query"
    echo "Fetching $num_results results"
    run_arxiv_query "$query" "$num_results"

    deactivate_venv
}

# Run the main function
main "$@"