package org.example.dw21130558_mxt.model.datawarehouse;
import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.LocalDate;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Entity
@Table(name = "productDim")
public class ProductDim {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "product_sk")
    private Integer productSk;

    @Column(name = "id")
    private String id;

    @Column(name = "name")
    private String name;

    @Column(name = "price", precision = 15, scale = 2)
    private BigDecimal price;

    @Column(name = "priceSale", precision = 15, scale = 2)
    private BigDecimal priceSale;

    @Column(name = "brand")
    private String brand;

    @Column(name = "color")
    private String color;

    @Column(name = "size")
    private String size;

    @Column(name = "status")
    private String status;

    @Column(name = "description_part1")
    private String descriptionPart1;

    @Column(name = "description_part2")
    private String descriptionPart2;

    @Column(name = "description_part3")
    private String descriptionPart3;

    @Column(name = "created_at", columnDefinition = "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    private LocalDateTime createdAt;

    @Column(name = "isDelete")
    private Boolean isDelete = false;

    @Column(name = "date_delete")
    private LocalDate dateDelete;

    @Column(name = "date_insert", columnDefinition = "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    private LocalDateTime dateInsert;

    @Column(name = "expired_date", columnDefinition = "DATE DEFAULT '9999-12-31'")
    private LocalDate expiredDate;

    @ManyToOne
    @JoinColumn(name = "date_sk", referencedColumnName = "date_sk")
    private DateDim dateDim;


}