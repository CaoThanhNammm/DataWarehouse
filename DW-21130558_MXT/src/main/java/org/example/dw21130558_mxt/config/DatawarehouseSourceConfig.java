package org.example.dw21130558_mxt.config;

import jakarta.persistence.EntityManagerFactory;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.jdbc.DataSourceBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.orm.jpa.JpaTransactionManager;
import org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;
import org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.annotation.EnableTransactionManagement;

import javax.sql.DataSource;
@Configuration
@EnableTransactionManagement
public class DatawarehouseSourceConfig {

    @Bean(name = "stDataSource")
    public DataSource stgDataSource() {
        return DataSourceBuilder.create()
                .url("jdbc:mysql://localhost:3306/staging")
                .username("root")
                .password("")
                .driverClassName("com.mysql.cj.jdbc.Driver")
                .build();
    }

    @Bean(name = "dwDataSource")
    public DataSource dwDataSource() {
        return DataSourceBuilder.create()
                .url("jdbc:mysql://localhost:3306/datawarehouse")
                .username("root")
                .password("")
                .driverClassName("com.mysql.cj.jdbc.Driver")
                .build();
    }

    @Bean(name = "dwJdbcTemplate")
    public JdbcTemplate dwJdbcTemplate(@Qualifier("stDataSource") DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }

    @Bean(name = "dmJdbcTemplate")
    public JdbcTemplate dmJdbcTemplate(@Qualifier("dwDataSource") DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }
    // Cấu hình EntityManagerFactory cho datamart
    @Bean(name = "dwEntityManagerFactory")
    public LocalContainerEntityManagerFactoryBean dmEntityManagerFactory(
            @Qualifier("dwDataSource") DataSource dataSource) {
        LocalContainerEntityManagerFactoryBean factoryBean = new LocalContainerEntityManagerFactoryBean();
        factoryBean.setDataSource(dataSource);
        factoryBean.setPackagesToScan("org.example.dw21130558_mxt.model.datawarehouse"); // Thư mục chứa các thực thể JPA của bạn

        HibernateJpaVendorAdapter vendorAdapter = new HibernateJpaVendorAdapter();
        vendorAdapter.setGenerateDdl(true); // Tạo ddl tự động
        vendorAdapter.setShowSql(true); // Hiển thị SQL trong log (tùy chọn)

        factoryBean.setJpaVendorAdapter(vendorAdapter);
        factoryBean.setPersistenceUnitName("dwPU");

        return factoryBean;
    }

    // Cấu hình TransactionManager cho datamart (Sửa để sử dụng JpaTransactionManager thay vì JtaTransactionManager)
    @Bean(name = "dwTransactionManager")
    public PlatformTransactionManager dmTransactionManager(
            @Qualifier("dwEntityManagerFactory") EntityManagerFactory entityManagerFactory) {
        return new JpaTransactionManager(entityManagerFactory);
    }
}
