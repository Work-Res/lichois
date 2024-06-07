# Project Documentation

## Project Overview
### The scope of the project is to address needs and functionalities of a comprehensive system for managing work and residence permits, facilitating investigations, citizenship and all occupational health and safety related services.

## Project Objectives
- To create robust api endpoints for the LICHOIS system.
- To document browsable api's using swagger.

## Repository Overview
| Repository Name | Repository Description |
| ----------- | ----------- |
| LICHOIS | Labour, Immigration, Citizenship and Occupational Health Integrated Service |

## Technologies
- Python
- Django ( admin site, ORM, url mappings)
- Django Rest
- Django Auth LDAP
- JWT (Java web tokens)
- Microsoft Graph API
- haystack
- Swagger

## File Structure Methodology

The project structure follows a **modular** or **feature-based** file organization methodology. Each directory within the main application directory represents a specific feature or module of the application.

### Benefits

1. **Separation of Concerns**: Each module or feature is isolated, making the codebase easier to understand and maintain. This structure promotes encapsulation and modularity.
2. **Scalability**: Adding new features or modules is simple which does not affect much the existing structure.
3. **Team Collaboration**: Different teams or team members can work on different modules independently, reducing the chances of merge conflicts and making version control more manageable.
4. **Testing**: Unit tests can be organized within each module, making it easier to test and troubleshoot individual features.

### Disadvantages

1. **Duplication**: Common functionality might be duplicated across modules. For example, utility functions or shared components might be re-implemented in multiple places.
2. **Inter-module Communication**: If modules are not well-defined, communication between modules can become complex, leading to tightly coupled components.
3. **Codebase Understanding**: For new developers, navigating through multiple directories to understand the codebase can be daunting.


## Directory Structure

- The repository or application follows a modular or feature-based file organization methodology.
