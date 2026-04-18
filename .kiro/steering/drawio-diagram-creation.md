---
inclusion: fileMatch
fileMatchPattern: "**/*.drawio,**/diagrams/**/*.md"
---

# Draw.io Diagram Creation Guide

## Overview

This document provides comprehensive guidelines for creating Draw.io diagrams as XML files programmatically. Draw.io (diagrams.net) uses an XML-based format that can be generated directly without using the GUI.

## Draw.io XML File Structure

### Basic File Format

Draw.io files (.drawio) are XML files with the following structure:

```xml
<mxfile host="app.diagrams.net" modified="2025-01-16T00:00:00.000Z" agent="5.0" version="22.1.0">
  <diagram name="Page-1" id="unique-diagram-id">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <!-- Your diagram elements go here -->
        
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### Key Elements

1. **mxfile**: Root element containing metadata
2. **diagram**: Container for a single diagram page
3. **mxGraphModel**: Defines the canvas and grid settings
4. **root**: Contains all diagram elements
5. **mxCell**: Individual shapes, connectors, and groups

## Creating Diagram Elements

### Basic Shape (Rectangle)

```xml
<mxCell id="shape1" value="Lambda Function" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>
```

**Attributes**:
- `id`: Unique identifier
- `value`: Text label
- `style`: Visual styling (colors, borders, etc.)
- `vertex="1"`: Indicates this is a shape (not a connector)
- `parent="1"`: Parent container

**Geometry**:
- `x`, `y`: Position on canvas
- `width`, `height`: Dimensions

### Connector (Arrow)

```xml
<mxCell id="edge1" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#000000;" edge="1" parent="1" source="shape1" target="shape2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

**Attributes**:
- `edge="1"`: Indicates this is a connector
- `source`: ID of source shape
- `target`: ID of target shape
- `edgeStyle`: Routing style (orthogonal, straight, curved)

### AWS Service Icons

AWS services can be represented using images:

```xml
<mxCell id="lambda1" value="Lambda" style="sketch=0;points=[[0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[0,1,0],[0.25,1,0],[0.5,1,0],[0.75,1,0],[1,1,0],[0,0.25,0],[0,0.5,0],[0,0.75,0],[1,0.25,0],[1,0.5,0],[1,0.75,0]];outlineConnect=0;fontColor=#232F3E;gradientColor=#F78E04;gradientDirection=north;fillColor=#D05C17;strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;" vertex="1" parent="1">
  <mxGeometry x="200" y="200" width="78" height="78" as="geometry"/>
</mxCell>
```

### Container/Group (Subgraph)

```xml
<mxCell id="group1" value="VPC" style="swimlane;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;" vertex="1" parent="1">
  <mxGeometry x="50" y="50" width="400" height="300" as="geometry"/>
</mxCell>

<!-- Child elements have parent="group1" -->
<mxCell id="child1" value="Subnet" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="group1">
  <mxGeometry x="20" y="40" width="120" height="60" as="geometry"/>
</mxCell>
```

## Common Styles

### Colors

```
fillColor=#dae8fc    (Light blue)
strokeColor=#6c8ebf  (Dark blue border)
fontColor=#000000    (Black text)
```

### AWS Service Colors

```
Lambda:     fillColor=#D05C17;gradientColor=#F78E04
DynamoDB:   fillColor=#2E73B8;gradientColor=#5294CF
S3:         fillColor=#277116;gradientColor=#60A337
API Gateway: fillColor=#945DF2;gradientColor=#B07FFF
```

### Shape Styles

```
Rectangle:  rounded=0;whiteSpace=wrap;html=1
Rounded:    rounded=1;whiteSpace=wrap;html=1
Ellipse:    ellipse;whiteSpace=wrap;html=1
Diamond:    rhombus;whiteSpace=wrap;html=1
```

### Edge Styles

```
Straight:     edgeStyle=none
Orthogonal:   edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1
Curved:       edgeStyle=curved;rounded=1
```

## Creating AWS Architecture Diagrams

### Template Structure

```xml
<mxfile>
  <diagram name="AWS Architecture">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <!-- VPC Container -->
        <mxCell id="vpc" value="VPC" style="swimlane;..." vertex="1" parent="1">
          <mxGeometry x="50" y="50" width="700" height="500" as="geometry"/>
        </mxCell>
        
        <!-- Public Subnet -->
        <mxCell id="public-subnet" value="Public Subnet" style="swimlane;..." vertex="1" parent="vpc">
          <mxGeometry x="20" y="40" width="300" height="200" as="geometry"/>
        </mxCell>
        
        <!-- Lambda in Public Subnet -->
        <mxCell id="lambda1" value="Lambda" style="...aws4.lambda..." vertex="1" parent="public-subnet">
          <mxGeometry x="100" y="60" width="78" height="78" as="geometry"/>
        </mxCell>
        
        <!-- Private Subnet -->
        <mxCell id="private-subnet" value="Private Subnet" style="swimlane;..." vertex="1" parent="vpc">
          <mxGeometry x="20" y="260" width="300" height="200" as="geometry"/>
        </mxCell>
        
        <!-- DynamoDB in Private Subnet -->
        <mxCell id="dynamodb1" value="DynamoDB" style="...aws4.dynamodb..." vertex="1" parent="private-subnet">
          <mxGeometry x="100" y="60" width="78" height="78" as="geometry"/>
        </mxCell>
        
        <!-- Connection -->
        <mxCell id="edge1" style="edgeStyle=orthogonalEdgeStyle;..." edge="1" parent="vpc" source="lambda1" target="dynamodb1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Programmatic Creation Guidelines

### ID Generation

- Use descriptive IDs: `lambda-ingest`, `dynamodb-docs`, `vpc-main`
- Ensure uniqueness across the entire diagram
- Use consistent naming patterns

### Positioning

- Grid size: 10px (align to grid)
- Standard spacing: 50px between elements
- Container padding: 20px from edges
- Vertical flow: Top to bottom
- Horizontal flow: Left to right

### Sizing

**Standard Sizes**:
- AWS Service Icon: 78x78
- Small Box: 120x60
- Medium Box: 160x80
- Large Box: 200x100
- Container: 400x300 minimum

### Layering

- Containers (VPC, Subnets): Lowest layer
- Services and components: Middle layer
- Connectors: Top layer
- Labels: Highest layer

## Best Practices

1. **Use Consistent Styling**: Define style constants and reuse them
2. **Logical Grouping**: Use containers for related components
3. **Clear Labels**: All elements should have descriptive labels
4. **Proper Spacing**: Maintain consistent spacing between elements
5. **Connection Points**: Use proper source/target references
6. **AWS Icons**: Use official AWS icon styles when available
7. **Color Coding**: Use consistent colors for component types
8. **Documentation**: Add comments in XML for complex sections

## Design Rules for Visual Clarity

### Background and Contrast

1. **Page Background**: Always use white background (`background="#FFFFFF"` in mxGraphModel)
   - Ensures maximum readability and print compatibility
   - Provides clean, professional appearance

2. **Text Color**: Use dark text for maximum contrast against light backgrounds
   - Default text: `fontColor="#000000"` (black) or `fontColor="#333333"` (dark gray)
   - Only use white text (`fontColor="#FFFFFF"`) when element has dark background
   - AWS service icons with dark fills should use their native light text colors

3. **Shape Text Colors**:
   - Light backgrounds (pastels): Use `fontColor="#000000"` (black)
   - Dark backgrounds: Use `fontColor="#FFFFFF"` (white)
   - Examples:
     - `fillColor=#d5e8d4` (light green) → `fontColor=#000000`
     - `fillColor=#277116` (dark green) → `fontColor=#277116` or white for contrast

### Connector Styling

1. **Connector Colors Match Source**: Connector stroke color should match the color of the object it originates from
   - S3 (green) connector: `strokeColor=#277116`
   - EventBridge (pink) connector: `strokeColor=#BC1356`
   - CloudWatch (orange) connector: `strokeColor=#D05C17`
   - Generic/neutral connectors: `strokeColor=#000000` (black) or `strokeColor=#666666` (gray)

2. **Connector Label Backgrounds**: No background for connector labels
   - Use `labelBackgroundColor=none` to keep labels transparent
   - Ensures labels don't obscure diagram elements
   - Maintains clean visual appearance

3. **Connector Label Positioning**: Text should be positioned on top of connector line
   - Horizontal connectors: `labelPosition=center;verticalLabelPosition=top;align=center;verticalAlign=bottom`
   - Vertical connectors: `labelPosition=center;verticalLabelPosition=top;align=center;verticalAlign=bottom;horizontal=0`
   - This places text above the line for horizontal connectors
   - For vertical connectors, text should be vertically aligned and positioned to the left of the connector

4. **Connector Label Colors**: Match connector stroke color or use contrasting color
   - If connector is colored (e.g., `strokeColor=#BC1356`), use same color for label: `fontColor=#BC1356`
   - If connector is neutral (black/gray), use black text: `fontColor=#000000`
   - Ensures visual consistency and clear association between connector and label

### Example: Properly Styled Connector

```xml
<!-- Horizontal connector with label on top -->
<mxCell id="arrow1" value="Route Events" 
  style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#BC1356;fontSize=11;fontStyle=1;labelBackgroundColor=none;fontColor=#BC1356;labelPosition=center;verticalLabelPosition=top;align=center;verticalAlign=bottom;" 
  edge="1" parent="1" source="eventbridge" target="rules-box">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- Vertical connector with label to the left -->
<mxCell id="arrow2" value="Event Metrics" 
  style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#D05C17;fontSize=11;fontStyle=1;dashed=1;labelBackgroundColor=none;fontColor=#BC1356;labelPosition=center;verticalLabelPosition=top;align=center;verticalAlign=bottom;horizontal=0;" 
  edge="1" parent="1" source="eventbridge" target="cloudwatch">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="570" y="350"/>
    </Array>
  </mxGeometry>
</mxCell>
```

### Color Palette Guidelines

**Light Backgrounds (use black text)**:
- `#d5e8d4` (light green) - ObjectCreated events
- `#ffe6cc` (light orange) - ObjectRemoved events
- `#dae8fc` (light blue) - ObjectModified events
- `#fff2cc` (light yellow) - Warnings/notes
- `#e1d5e7` (light purple) - Metrics/monitoring
- `#f5f5f5` (light gray) - Containers/groups

**Dark Backgrounds (use white or light text)**:
- `#277116` (dark green) - S3 service icon
- `#BC1356` (dark pink) - EventBridge/Step Functions icons
- `#D05C17` (dark orange) - CloudWatch icon
- `#2E73B8` (dark blue) - DynamoDB icon

### Accessibility Considerations

1. **Contrast Ratio**: Maintain minimum 4.5:1 contrast ratio between text and background
2. **Color Blindness**: Don't rely solely on color to convey information; use labels and patterns
3. **Print Compatibility**: White background with dark text ensures diagrams print clearly
4. **Screen Readability**: High contrast improves readability on all screen types

## Example: Complete Lambda + DynamoDB Diagram

```xml
<mxfile host="app.diagrams.net">
  <diagram name="Lambda-DynamoDB">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <!-- API Gateway -->
        <mxCell id="apigw" value="API Gateway" style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#945DF2;strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;" vertex="1" parent="1">
          <mxGeometry x="100" y="200" width="78" height="78" as="geometry"/>
        </mxCell>
        
        <!-- Lambda Function -->
        <mxCell id="lambda" value="Lambda Function" style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#D05C17;strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;" vertex="1" parent="1">
          <mxGeometry x="300" y="200" width="78" height="78" as="geometry"/>
        </mxCell>
        
        <!-- DynamoDB -->
        <mxCell id="dynamodb" value="DynamoDB" style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#2E73B8;strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.dynamodb;" vertex="1" parent="1">
          <mxGeometry x="500" y="200" width="78" height="78" as="geometry"/>
        </mxCell>
        
        <!-- Connection: API Gateway to Lambda -->
        <mxCell id="edge1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#000000;" edge="1" parent="1" source="apigw" target="lambda">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <!-- Connection: Lambda to DynamoDB -->
        <mxCell id="edge2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#000000;" edge="1" parent="1" source="lambda" target="dynamodb">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Common Errors and Fixes

### Error: "Not a diagram file" - Cannot read properties of null (reading 'getAttribute')

This error occurs when Draw.io XML files contain invalid XML syntax or unsupported elements. Common causes and fixes:

#### 1. HTML Comments in XML

**Problem**: Draw.io XML does not support HTML-style comments (`<!-- -->`)

**Broken Example**:
```xml
<root>
  <mxCell id="0"/>
  <mxCell id="1" parent="0"/>
  
  <!-- This is a comment -->
  <mxCell id="shape1" value="Box" vertex="1" parent="1">
    <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
  </mxCell>
</root>
```

**Fixed Example**:
```xml
<root>
  <mxCell id="0"/>
  <mxCell id="1" parent="0"/>
  
  <mxCell id="shape1" value="Box" vertex="1" parent="1">
    <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
  </mxCell>
</root>
```

**Solution**: Remove all HTML comments (`<!-- -->`) from the XML file. Use descriptive IDs and proper XML structure instead.

#### 2. Invalid Host Attribute

**Problem**: The `host` attribute in the `<mxfile>` tag must be a valid value recognized by Draw.io

**Broken Example**:
```xml
<mxfile host="65bd71144e">
```

**Fixed Example**:
```xml
<mxfile host="app.diagrams.net">
```

**Valid host values**:
- `app.diagrams.net` (recommended)
- `www.draw.io`
- `embed.diagrams.net`

#### 3. Inconsistent Geometry Tag Format

**Problem**: Geometry tags must be self-closing and include `as="geometry"` attribute

**Broken Example**:
```xml
<mxGeometry x="100" y="100" width="120" height="60"/>
```

**Fixed Example**:
```xml
<mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
```

#### 4. Missing Required Attributes

**Problem**: mxCell elements require specific attributes depending on whether they are shapes or edges

**For Shapes (vertex)**:
```xml
<mxCell id="unique-id" value="Label" style="..." vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>
```

**For Edges (connectors)**:
```xml
<mxCell id="unique-id" value="Label" style="..." edge="1" parent="1" source="id1" target="id2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

Required attributes:
- `id`: Unique identifier (string)
- `vertex="1"` OR `edge="1"`: Specifies element type
- `parent`: Parent container ID (usually "1" or a group ID)

For edges, also required:
- `source`: ID of source shape
- `target`: ID of target shape

#### 5. Character Encoding Issues

**Problem**: Special characters must be properly encoded in XML

**Broken Example**:
```xml
<mxCell id="text1" value="Kanri (管理)&#xa;Audit & Analysis" ...>
```

**Fixed Example**:
```xml
<mxCell id="text1" value="Kanri (管理)&#xa;Audit &amp; Analysis" ...>
```

**XML Entity Encoding**:
- `&` → `&amp;`
- `<` → `&lt;`
- `>` → `&gt;`
- `"` → `&quot;`
- `'` → `&apos;`
- Line break: `&#xa;`

#### 6. Malformed XML Structure

**Problem**: XML tags must be properly closed and nested

**Common Issues**:
- Missing closing tags
- Self-closing tags without `/>`
- Attributes without proper quotes
- Mixed single and double closing tag formats

**Broken Example**:
```xml
<mxCell id="0"/>
<mxCell id="1" parent="0" />
```

**Fixed Example** (choose one format and be consistent):
```xml
<mxCell id="0" />
<mxCell id="1" parent="0" />
```

### Troubleshooting Steps

When encountering "Not a diagram file" error:

1. **Validate XML Syntax**: Use an XML validator to check for syntax errors
2. **Check for HTML Comments**: Search for `<!--` and remove all instances
3. **Verify Host Attribute**: Ensure `<mxfile host="app.diagrams.net">`
4. **Validate Element Structure**:
   - All `<mxCell>` elements have required attributes
   - Geometry tags include `as="geometry"`
   - Proper encoding of special characters
5. **Test with Minimal File**: Create a minimal valid file and add elements incrementally
6. **Compare with Working Example**: Use the template provided in this document as reference

### Minimal Valid Draw.io File

Use this as a starting template for troubleshooting:

```xml
<mxfile host="app.diagrams.net">
  <diagram id="test-diagram" name="Test">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="2" value="Test Box" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="100" y="100" width="120" height="60" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

If this minimal file opens successfully, the Draw.io installation is working correctly. Gradually add your content back, testing after each addition to isolate the problematic element.

## Validation

After creating a Draw.io XML file:

1. **Open in Draw.io**: Load the file in https://app.diagrams.net/
2. **Check Rendering**: Verify all elements display correctly
3. **Test Connections**: Ensure arrows connect properly
4. **Verify Styling**: Check colors, fonts, and spacing
5. **Export Test**: Export as PNG to verify output quality
6. **XML Validation**: Ensure no HTML comments or malformed XML

## File Naming Convention

- Use descriptive names: `01-system-architecture.drawio`
- Include sequence numbers for ordering
- Use kebab-case
- Extension: `.drawio` or `.xml`

---

**Created**: 2025-01-16  
**Purpose**: Enable programmatic creation of Draw.io diagrams for AWS architecture documentation  
**Maintained By**: Platform Engineering Team
