package com.example.loadtodatamart.config;

import jakarta.persistence.EntityManagerFactory;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.jdbc.DataSourceBuilder;
import org.springframework.boot.orm.jpa.EntityManagerFactoryBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;
import org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.annotation.EnableTransactionManagement;
import org.springframework.orm.jpa.JpaTransactionManager;

import javax.sql.DataSource;

@Configuration
@EnableTransactionManagement
public class DataMartSourceConfig {

    @Bean(name = "dwDataSource")
    public DataSource dwDataSource() {
        return DataSourceBuilder.create()
                .url("jdbc:mysql://localhost:3306/datawarehouse")
                .username("root")
                .password("")
                .driverClassName("com.mysql.cj.jdbc.Driver")
                .build();
    }

    @Bean(name = "dmDataSource")
    public DataSource dmDataSource() {
        return DataSourceBuilder.create()
                .url("jdbc:mysql://localhost:3306/datamart")
                .username("root")
                .password("")
                .driverClassName("com.mysql.cj.jdbc.Driver")
                .build();
    }

    @Bean(name = "dwJdbcTemplate")
    public JdbcTemplate dwJdbcTemplate(@Qualifier("dwDataSource") DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }

    @Bean(name = "dmJdbcTemplate")
    public JdbcTemplate dmJdbcTemplate(@Qualifier("dmDataSource") DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }

    // Cấu hình EntityManagerFactory cho datamart
    @Bean(name = "dmEntityManagerFactory")
    public LocalContainerEntityManagerFactoryBean dmEntityManagerFactory(
            @Qualifier("dmDataSource") DataSource dataSource) {
        LocalContainerEntityManagerFactoryBean factoryBean = new LocalContainerEntityManagerFactoryBean();
        factoryBean.setDataSource(dataSource);
        factoryBean.setPackagesToScan("com.example.loadtodatamart.model.datamart"); // Thư mục chứa các thực thể JPA của bạn

        HibernateJpaVendorAdapter vendorAdapter = new HibernateJpaVendorAdapter();
        vendorAdapter.setGenerateDdl(true); // Tạo ddl tự động
        vendorAdapter.setShowSql(true);

        factoryBean.setJpaVendorAdapter(vendorAdapter);
        factoryBean.setPersistenceUnitName("datamartPU");

        return factoryBean;
    }

    // Cấu hình TransactionManager cho datamart (Sửa để sử dụng JpaTransactionManager thay vì JtaTransactionManager)
    @Bean(name = "dmTransactionManager")
    public PlatformTransactionManager dmTransactionManager(
            @Qualifier("dmEntityManagerFactory") EntityManagerFactory entityManagerFactory) {
        return new JpaTransactionManager(entityManagerFactory);
    }
}
